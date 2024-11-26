from datetime import datetime

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import pgettext
from django.views import View

from ...auth.decorators import login_required
from ...categories.models import Category
from ...htmx.response import htmx_redirect
from ...permissions.privatethreads import check_reply_private_thread_permission
from ...permissions.threads import check_reply_thread_permission
from ...posting.formsets import (
    PostingFormset,
    ReplyPrivateThreadFormset,
    ReplyThreadFormset,
    get_reply_private_thread_formset,
    get_reply_thread_formset,
)
from ...posting.state import (
    ReplyPrivateThreadState,
    ReplyThreadState,
    get_reply_private_thread_state,
    get_reply_thread_state,
)
from ...readtracker.tracker import (
    get_thread_read_time,
    mark_thread_read,
    mark_category_read,
)
from ...readtracker.privatethreads import unread_private_threads_exist
from ...readtracker.threads import is_category_read
from ..hooks import (
    get_reply_private_thread_page_context_data_hook,
    get_reply_thread_page_context_data_hook,
)
from ..models import Post, Thread
from .redirect import private_thread_post_redirect, thread_post_redirect
from .generic import PrivateThreadView, ThreadView


class ReplyView(View):
    thread_annotate_read_time: bool = True

    template_name: str
    template_name_htmx: str
    template_name_quick_reply: str = "misago/quick_reply/index.html"

    def get(self, request: HttpRequest, id: int, slug: str) -> HttpResponse:
        thread = self.get_thread(request, id)
        formset = self.get_formset(request, thread)
        return self.render(request, thread, formset)

    def post(self, request: HttpRequest, id: int, slug: str) -> HttpResponse:
        thread = self.get_thread(request, id)
        state = self.get_state(request, thread)
        formset = self.get_formset(request, thread)
        formset.update_state(state)

        if request.POST.get("preview"):
            return self.render(request, thread, formset, state.post.parsed)

        if not formset.is_valid():
            return self.render(request, thread, formset)

        state.save()

        messages.success(request, pgettext("thread reply posted", "Reply posted"))

        if self.is_quick_reply(request):
            return self.post_quick_reply(request, thread, state)

        redirect = self.get_redirect_response(request, state.thread, state.post)
        if request.is_htmx:
            return htmx_redirect(redirect.headers["location"])

        return redirect

    def post_quick_reply(
        self, request: HttpRequest, thread: Thread, state: ReplyThreadState
    ) -> HttpResponse:
        # TODO: remove once we no longer serialize user object to preload JSON data
        request.user.refresh_from_db()

        request.method = "GET"
        formset = self.get_formset(request, thread)
        request.method = "POST"

        feed = self.get_posts_feed(request, thread, [state.post])
        feed.set_animated_posts([state.post.id])
        feed.set_unread_posts([state.post.id])

        response = self.render(request, thread, formset, feed=feed.get_feed_data())

        # Is thread (excluding last reply) read?
        read_time = get_thread_read_time(request, thread)
        thread_is_read = not (
            self.get_thread_posts_queryset(request, thread)
            .exclude(id=state.post.id)
            .filter(posted_on__gt=read_time)
            .exists()
        )

        # Mark posted quick reply as read
        if thread_is_read:
            mark_thread_read(request.user, thread, state.timestamp)
            if self.is_category_read(
                request, state.category, thread.category_read_time
            ):
                mark_category_read(request.user, state.category, force_update=True)

        return response

    def get_state(self, request: HttpRequest, thread: Thread) -> ReplyThreadState:
        raise NotImplementedError()

    def get_formset(self, request: HttpRequest, thread: Thread) -> PostingFormset:
        raise NotImplementedError()

    def render(
        self,
        request: HttpRequest,
        thread: Thread,
        formset: PostingFormset,
        preview: str | None = None,
        feed: list[dict] | None = None,
    ):
        context = self.get_context_data(request, thread, formset)
        context["preview"] = preview
        context["new_feed"] = feed

        if self.is_quick_reply(request):
            template_name = self.template_name_quick_reply
        elif request.is_htmx:
            template_name = self.template_name_htmx
        else:
            template_name = self.template_name

        return render(request, template_name, context)

    def get_context_data(
        self, request: HttpRequest, thread: Thread, formset: PostingFormset
    ) -> dict:
        raise NotImplementedError()

    def get_context_data_action(
        self, request: HttpRequest, thread: Thread, formset: PostingFormset
    ) -> dict:
        return {
            "thread": thread,
            "formset": formset,
            "url": self.get_form_url(request, thread),
            "template_name_htmx": self.template_name_htmx,
        }

    def get_form_url(self, request: HttpRequest, thread: Thread) -> None:
        raise NotImplementedError

    def get_redirect_response(
        self, request: HttpRequest, thread: Thread, post: Post
    ) -> HttpResponse:
        raise NotImplementedError()

    def is_quick_reply(self, request: HttpRequest) -> bool:
        return request.is_htmx and request.POST.get("quick_reply")

    def is_category_read(
        self, request: HttpRequest, category: Category, read_time: datetime | None
    ) -> bool:
        raise NotImplementedError()


class ReplyThreadView(ReplyView, ThreadView):
    template_name: str = "misago/reply_thread/index.html"
    template_name_htmx: str = "misago/reply_thread/form.html"

    def get_thread(self, request: HttpRequest, thread_id: int) -> Thread:
        thread = super().get_thread(request, thread_id)
        check_reply_thread_permission(request.user_permissions, thread.category, thread)
        return thread

    def get_state(self, request: HttpRequest, thread: Thread) -> ReplyThreadState:
        return get_reply_thread_state(request, thread)

    def get_formset(self, request: HttpRequest, thread: Thread) -> ReplyThreadFormset:
        return get_reply_thread_formset(request, thread)

    def get_context_data(
        self, request: HttpRequest, thread: Thread, formset: ReplyThreadFormset
    ) -> dict:
        return get_reply_thread_page_context_data_hook(
            self.get_context_data_action, request, thread, formset
        )

    def get_form_url(self, request: HttpRequest, thread: Thread) -> None:
        return reverse(
            "misago:reply-thread", kwargs={"id": thread.id, "slug": thread.slug}
        )

    def get_redirect_response(
        self, request: HttpRequest, thread: Thread, post: Post
    ) -> HttpResponse:
        return thread_post_redirect(
            request, id=thread.id, slug=thread.slug, post=post.id
        )

    def is_category_read(
        self, request: HttpRequest, category: Category, read_time: datetime | None
    ) -> bool:
        return is_category_read(request, category, read_time)


class ReplyPrivateThreadView(ReplyView, PrivateThreadView):
    template_name: str = "misago/reply_private_thread/index.html"
    template_name_htmx: str = "misago/reply_private_thread/form.html"

    def get_thread(self, request: HttpRequest, thread_id: int) -> Thread:
        thread = super().get_thread(request, thread_id)
        check_reply_private_thread_permission(request.user_permissions, thread)
        return thread

    def get_state(
        self, request: HttpRequest, thread: Thread
    ) -> ReplyPrivateThreadState:
        return get_reply_private_thread_state(request, thread)

    def get_formset(
        self, request: HttpRequest, thread: Thread
    ) -> ReplyPrivateThreadFormset:
        return get_reply_private_thread_formset(request, thread)

    def get_context_data(
        self, request: HttpRequest, thread: Thread, formset: ReplyPrivateThreadFormset
    ) -> dict:
        return get_reply_private_thread_page_context_data_hook(
            self.get_context_data_action, request, thread, formset
        )

    def get_form_url(self, request: HttpRequest, thread: Thread) -> None:
        return reverse(
            "misago:reply-private-thread", kwargs={"id": thread.id, "slug": thread.slug}
        )

    def get_redirect_response(
        self, request: HttpRequest, thread: Thread, post: Post
    ) -> HttpResponse:
        return private_thread_post_redirect(
            request, id=thread.id, slug=thread.slug, post=post.id
        )

    def is_category_read(
        self, request: HttpRequest, category: Category, read_time: datetime | None
    ) -> bool:
        return not unread_private_threads_exist(request, category, read_time)


def reply_thread_login_required(f):
    return login_required(
        pgettext(
            "reply thread page",
            "Sign in to reply to threads",
        )
    )(f)


reply_thread = reply_thread_login_required(ReplyThreadView.as_view())
reply_private_thread = reply_thread_login_required(ReplyPrivateThreadView.as_view())
