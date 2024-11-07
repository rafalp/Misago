from django.http import HttpRequest, HttpResponse
from django.views import View
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import pgettext

from ...auth.decorators import login_required
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
from ..models import Thread
from .redirect import get_redirect_to_post_response
from .generic import PrivateThreadView, ThreadView


def reply_thread_login_required():
    return login_required(
        pgettext(
            "reply thread page",
            "Sign in to reply to threads",
        )
    )


class ReplyView(View):
    template_name: str

    @method_decorator(reply_thread_login_required())
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

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
            context = self.get_context_data(request, thread, formset)
            context["preview"] = state.post.parsed
            return render(request, self.template_name, context)

        if not formset.is_valid():
            return self.render(request, thread, formset)

        state.save()
        return get_redirect_to_post_response(request, state.post)

    def get_state(self, request: HttpRequest, thread: Thread) -> ReplyThreadState:
        raise NotImplementedError()

    def get_formset(self, request: HttpRequest, thread: Thread) -> ReplyThreadFormset:
        raise NotImplementedError()

    def render(self, request: HttpRequest, thread: Thread, formset: ReplyThreadFormset):
        return render(
            request, self.template_name, self.get_context_data(request, thread, formset)
        )

    def get_context_data(
        self, request: HttpRequest, thread: Thread, formset: ReplyThreadFormset
    ) -> dict:
        raise NotImplementedError()


class ThreadReplyView(ReplyView, ThreadView):
    template_name: str = "misago/reply_thread/index.html"

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
        return {"thread": thread, "formset": formset}


class PrivateThreadReplyView(ReplyView, PrivateThreadView):
    template_name: str = "misago/reply_thread/index.html"

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
        self, request: HttpRequest, thread: Thread, formset: ReplyThreadFormset
    ) -> dict:
        return get_reply_private_thread_page_context_data_hook(
            self.get_context_data_action, request, thread, formset
        )

    def get_context_data_action(
        self, request: HttpRequest, thread: Thread, formset: ReplyPrivateThreadFormset
    ) -> dict:
        return {"thread": thread, "formset": formset}


thread_reply = ThreadReplyView.as_view()
private_thread_reply = PrivateThreadReplyView.as_view()
