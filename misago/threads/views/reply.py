from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.shortcuts import render
from django.utils.translation import pgettext

from ...auth.decorators import login_required
from ...htmx.response import htmx_redirect
from ...permissions.privatethreads import check_reply_private_thread_permission
from ...permissions.threads import check_reply_thread_permission
from ...posting.formsets import (
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
from ..hooks import (
    get_reply_private_thread_page_context_data_hook,
    get_reply_thread_page_context_data_hook,
)
from ..models import Post, Thread
from .redirect import private_thread_post_redirect, thread_post_redirect
from .generic import PrivateThreadView, ThreadView


class ReplyView(View):
    template_name: str
    template_name_htmx: str

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

        redirect = self.get_redirect_response(request, state.thread, state.post)
        if request.is_htmx:
            return htmx_redirect(redirect.headers["location"])

        return redirect

    def get_state(self, request: HttpRequest, thread: Thread) -> ReplyThreadState:
        raise NotImplementedError()

    def get_formset(self, request: HttpRequest, thread: Thread) -> ReplyThreadFormset:
        raise NotImplementedError()

    def render(
        self,
        request: HttpRequest,
        thread: Thread,
        formset: ReplyThreadFormset,
        preview: str | None = None,
    ):
        context = self.get_context_data(request, thread, formset)
        context["preview"] = preview

        if request.is_htmx:
            template_name = self.template_name_htmx
        else:
            template_name = self.template_name

        return render(request, template_name, context)

    def get_context_data(
        self, request: HttpRequest, thread: Thread, formset: ReplyThreadFormset
    ) -> dict:
        raise NotImplementedError()

    def get_redirect_response(
        self, request: HttpRequest, thread: Thread, post: Post
    ) -> HttpResponse:
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

    def get_context_data_action(
        self, request: HttpRequest, thread: Thread, formset: ReplyThreadFormset
    ) -> dict:
        return {
            "thread": thread,
            "formset": formset,
            "template_name_htmx": self.template_name_htmx,
        }

    def get_redirect_response(
        self, request: HttpRequest, thread: Thread, post: Post
    ) -> HttpResponse:
        return thread_post_redirect(
            request, id=thread.id, slug=thread.slug, post=post.id
        )


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

    def get_context_data_action(
        self, request: HttpRequest, thread: Thread, formset: ReplyPrivateThreadFormset
    ) -> dict:
        return {
            "thread": thread,
            "formset": formset,
            "template_name_htmx": self.template_name_htmx,
        }

    def get_redirect_response(
        self, request: HttpRequest, thread: Thread, post: Post
    ) -> HttpResponse:
        return private_thread_post_redirect(
            request, id=thread.id, slug=thread.slug, post=post.id
        )


def reply_thread_login_required(f):
    return login_required(
        pgettext(
            "reply thread page",
            "Sign in to reply to threads",
        )
    )(f)


reply_thread = reply_thread_login_required(ReplyThreadView.as_view())
reply_private_thread = reply_thread_login_required(ReplyPrivateThreadView.as_view())
