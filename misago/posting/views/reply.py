from datetime import datetime, timedelta

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import pgettext
from django.views import View

from ...categories.models import Category
from ...htmx.response import htmx_redirect
from ...permissions.checkutils import check_permissions
from ...permissions.privatethreads import (
    check_edit_private_thread_post_permission,
    check_reply_private_thread_permission,
)
from ...permissions.threads import (
    check_edit_thread_post_permission,
    check_reply_thread_permission,
)
from ...privatethreads.views.backend import private_thread_backend
from ...privatethreads.views.generic import PrivateThreadView
from ...privatethreads.redirect import redirect_to_private_thread_post
from ...readtracker.tracker import (
    get_thread_read_time,
    mark_thread_read,
    mark_category_read,
)
from ...readtracker.privatethreads import unread_private_threads_exist
from ...readtracker.threads import is_category_read
from ...threads.models import Post, Thread
from ...threads.prefetch import prefetch_post_feed_related_objects
from ...threads.redirect import redirect_to_thread_post
from ...threads.views.backend import ViewBackend, thread_backend
from ...threads.views.generic import ThreadView
from ..hooks import (
    get_private_thread_reply_context_data_hook,
    get_thread_reply_context_data_hook,
)
from ..formsets import (
    Formset,
    PrivateThreadReplyFormset,
    ThreadReplyFormset,
    get_private_thread_reply_formset,
    get_thread_reply_formset,
)
from ..state import (
    PrivateThreadReplyState,
    ReplyState,
    ThreadReplyState,
    get_reply_private_thread_state,
    get_reply_thread_state,
)
from ..validators import validate_flood_control, validate_posted_contents


class ReplyView(View):
    backend: ViewBackend
    thread_annotate_read_time: bool = True

    template_name: str
    template_name_htmx: str
    template_name_quick_reply: str = "misago/quick_reply/index.html"

    def get(self, request: HttpRequest, thread_id: int, slug: str) -> HttpResponse:
        thread = self.get_thread(request, thread_id)
        initial_data = self.get_formset_initial_data(request, thread)
        formset = self.get_formset(request, thread, initial_data)
        return self.render(request, thread, formset)

    def post(self, request: HttpRequest, thread_id: int, slug: str) -> HttpResponse:
        thread = self.get_thread(request, thread_id)
        formset = self.get_formset(request, thread)

        if not formset.is_request_preview(request):
            last_post = self.get_last_post(request, thread)
        else:
            last_post = None

        state = self.get_state(request, thread, last_post)
        formset.update_state(state)

        if formset.is_request_preview(request):
            formset.clear_errors_in_preview()
            return self.render(request, thread, formset, state)

        if formset.is_request_upload(request):
            formset.clear_errors_in_upload()
            return self.render(request, thread, formset)

        if not self.is_valid(formset, state):
            return self.render(request, thread, formset)

        state.save()

        if state.is_merged:
            messages.success(
                request,
                pgettext(
                    "thread reply posted",
                    "Reply was automatically merged with the previous post",
                ),
            )
        else:
            messages.success(request, pgettext("thread reply posted", "Reply posted"))

        if self.is_quick_reply(request):
            return self.post_quick_reply(request, thread, state)

        redirect = self.get_redirect_response(request, state.thread, state.post)
        if request.is_htmx:
            return htmx_redirect(redirect.headers["location"])

        return redirect

    def post_quick_reply(
        self, request: HttpRequest, thread: Thread, state: ReplyState
    ) -> HttpResponse:
        # TODO: remove once we no longer serialize user object to preload JSON data
        request.user.refresh_from_db()

        request.method = "GET"
        formset = self.get_formset(request, thread)
        request.method = "POST"

        feed = self.get_post_feed(request, thread, [state.post])
        feed.set_animated_posts([state.post.id])

        counter_start = (
            self.get_thread_posts_queryset(request, state.thread)
            .filter(id__lt=state.post.id)
            .count()
        )
        feed.set_counter_start(counter_start)

        if not state.is_merged:
            feed.set_unread_posts([state.post.id])

        response = self.render(
            request,
            thread,
            formset,
            feed=feed.get_feed_data(),
            htmx_swap=state.is_merged,
        )

        if not state.is_merged:
            self.mark_reply_as_read(request, thread, state)

        return response

    def mark_reply_as_read(
        self, request: HttpRequest, thread: Thread, state: ReplyState
    ):
        # Is thread (excluding last reply) read?
        read_time = get_thread_read_time(request, thread)
        thread_is_read = not (
            self.get_thread_posts_queryset(request, thread)
            .exclude(id=state.post.id)
            .filter(posted_at__gt=read_time)
            .exists()
        )

        # Mark posted quick reply as read
        if thread_is_read:
            mark_thread_read(request.user, thread, state.timestamp)
            if self.is_category_read(
                request, state.category, thread.user_readcategory_time
            ):
                mark_category_read(request.user, state.category, force_update=True)

    def get_last_post(self, request: HttpRequest, thread: Thread) -> Post | None:
        merge_time = request.settings.merge_concurrent_posts
        if not merge_time:
            return None

        last_post = self.get_thread_posts_queryset(request, thread).last()

        if last_post.poster_id != request.user.id:
            return None

        if (timezone.now() - last_post.posted_at) > timedelta(minutes=merge_time):
            return False

        if last_post.is_hidden:
            return False

        last_post.thread = thread
        last_post.category = thread.category

        return last_post

    def get_state(
        self, request: HttpRequest, thread: Thread, post: Post | None
    ) -> ThreadReplyState:
        raise NotImplementedError()

    def get_formset(
        self, request: HttpRequest, thread: Thread, initial: dict | None = None
    ) -> Formset:
        raise NotImplementedError()

    def get_formset_initial_data(
        self, request: HttpRequest, thread: Thread
    ) -> dict | None:
        data = {}
        if quoted_post := self.get_quoted_post(request, thread):
            data["post"] = (
                f"[quote={quoted_post.poster_name}, post: {quoted_post.id}]"
                "\n"
                f"{quoted_post.original}"
                "\n"
                "[/quote]"
                "\n\n"
            )

        return data or None

    def get_quoted_post(self, request: HttpRequest, thread: Thread) -> Post | None:
        try:
            post_id = int(request.GET.get("quote") or 0)
        except (ValueError, TypeError):
            return None

        if not post_id:
            return None

        try:
            return self.backend.get_thread_post(
                request, thread, post_id, for_content=True
            )
        except (Http404, PermissionDenied):
            return None

    def is_valid(self, formset: Formset, state: ReplyState) -> bool:
        return (
            formset.is_valid()
            and (state.is_merged or validate_flood_control(formset, state))
            and validate_posted_contents(formset, state)
        )

    def render(
        self,
        request: HttpRequest,
        thread: Thread,
        formset: Formset,
        preview: ReplyState | None = None,
        feed: list[dict] | None = None,
        htmx_swap: bool = False,
    ):
        context = self.get_context_data(request, thread, formset)
        context["new_feed"] = feed
        context["htmx_swap"] = htmx_swap

        if preview:
            related_objects = prefetch_post_feed_related_objects(
                request.settings,
                request.user_permissions,
                [preview.post],
                categories=[thread.category],
                threads=[thread],
                attachments=preview.attachments,
            )

            context["preview"] = preview.post.parsed
            context["preview_rich_text_data"] = related_objects

        if self.is_quick_reply(request):
            template_name = self.template_name_quick_reply
        elif request.is_htmx:
            template_name = self.template_name_htmx
        else:
            template_name = self.template_name

        return render(request, template_name, context)

    def get_context_data(
        self, request: HttpRequest, thread: Thread, formset: Formset
    ) -> dict:
        raise NotImplementedError()

    def get_context_data_action(
        self, request: HttpRequest, thread: Thread, formset: Formset
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
        if not request.is_htmx:
            return False
        if request.method == "POST" and request.POST.get("quick_reply"):
            return True
        if request.method == "GET" and request.GET.get("quick_reply"):
            return True

        return False

    def is_category_read(
        self, request: HttpRequest, category: Category, read_time: datetime | None
    ) -> bool:
        raise NotImplementedError()


class ThreadReplyView(ReplyView, ThreadView):
    backend = thread_backend

    template_name: str = "misago/thread_reply/index.html"
    template_name_htmx: str = "misago/thread_reply/form.html"

    def get_thread(self, request: HttpRequest, thread_id: int) -> Thread:
        thread = super().get_thread(request, thread_id)
        check_reply_thread_permission(request.user_permissions, thread.category, thread)
        return thread

    def get_last_post(self, request: HttpRequest, thread: Thread) -> Post | None:
        if last_post := super().get_last_post(request, thread):
            with check_permissions() as can_edit_post:
                check_edit_thread_post_permission(
                    request.user_permissions, thread.category, thread, last_post
                )

            if can_edit_post:
                return last_post

        return None

    def get_state(
        self, request: HttpRequest, thread: Thread, post: Post | None
    ) -> ThreadReplyState:
        return get_reply_thread_state(request, thread, post)

    def get_formset(
        self, request: HttpRequest, thread: Thread, initial: dict | None = None
    ) -> ThreadReplyFormset:
        return get_thread_reply_formset(request, thread, initial)

    def get_context_data(
        self, request: HttpRequest, thread: Thread, formset: ThreadReplyFormset
    ) -> dict:
        return get_thread_reply_context_data_hook(
            self.get_context_data_action, request, thread, formset
        )

    def get_form_url(self, request: HttpRequest, thread: Thread) -> None:
        return reverse(
            "misago:thread-reply", kwargs={"thread_id": thread.id, "slug": thread.slug}
        )

    def get_redirect_response(
        self, request: HttpRequest, thread: Thread, post: Post
    ) -> HttpResponse:
        return redirect_to_thread_post(request, thread, post)

    def is_category_read(
        self, request: HttpRequest, category: Category, read_time: datetime | None
    ) -> bool:
        return is_category_read(request, category, read_time)


class PrivateThreadReplyView(ReplyView, PrivateThreadView):
    backend = private_thread_backend

    template_name: str = "misago/private_thread_reply/index.html"
    template_name_htmx: str = "misago/private_thread_reply/form.html"

    def get_thread(self, request: HttpRequest, thread_id: int) -> Thread:
        thread = super().get_thread(request, thread_id)
        check_reply_private_thread_permission(request.user_permissions, thread)
        return thread

    def get_last_post(self, request: HttpRequest, thread: Thread) -> Post | None:
        if last_post := super().get_last_post(request, thread):
            with check_permissions() as can_edit_post:
                check_edit_private_thread_post_permission(
                    request.user_permissions, thread.category, last_post
                )

            if can_edit_post:
                return last_post

        return None

    def get_state(
        self, request: HttpRequest, thread: Thread, post: Post | None
    ) -> PrivateThreadReplyState:
        return get_reply_private_thread_state(request, thread, post)

    def get_formset(
        self, request: HttpRequest, thread: Thread, initial: dict | None = None
    ) -> PrivateThreadReplyFormset:
        return get_private_thread_reply_formset(request, thread, initial)

    def get_context_data(
        self, request: HttpRequest, thread: Thread, formset: PrivateThreadReplyFormset
    ) -> dict:
        return get_private_thread_reply_context_data_hook(
            self.get_context_data_action, request, thread, formset
        )

    def get_form_url(self, request: HttpRequest, thread: Thread) -> None:
        return reverse(
            "misago:private-thread-reply",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )

    def get_redirect_response(
        self, request: HttpRequest, thread: Thread, post: Post
    ) -> HttpResponse:
        return redirect_to_private_thread_post(request, thread, post)

    def is_category_read(
        self, request: HttpRequest, category: Category, read_time: datetime | None
    ) -> bool:
        return not unread_private_threads_exist(request, category, read_time)
