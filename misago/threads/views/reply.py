from django.http import HttpRequest, HttpResponse
from django.views import View

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
from ..models import Thread
from .redirect import get_redirect_to_post_response
from .generic import PrivateThreadView, ThreadView


class ReplyView(View):
    def get(self, request: HttpRequest, id: int, slug: str) -> HttpResponse:
        thread = self.get_thread(request, id)
        formset = self.get_formset(request, thread)

    def post(self, request: HttpRequest, id: int, slug: str) -> HttpResponse:
        thread = self.get_thread(request, id)
        state = self.get_state(request, thread)
        formset = self.get_formset(request, thread)
        formset.update_state(state)

        if not formset.is_valid():
            raise ValueError([f.errors for f in formset.get_forms()])

        state.save()
        return get_redirect_to_post_response(request, state.post)

    def get_state(self, request: HttpRequest, thread: Thread) -> ReplyThreadState:
        raise NotImplementedError()

    def get_formset(self, request: HttpRequest, thread: Thread) -> ReplyThreadFormset:
        raise NotImplementedError()


class ThreadReplyView(ReplyView, ThreadView):
    def get_state(self, request: HttpRequest, thread: Thread) -> ReplyThreadState:
        return get_reply_thread_state(request, thread)

    def get_formset(self, request: HttpRequest, thread: Thread) -> ReplyThreadFormset:
        return get_reply_thread_formset(request, thread)


class PrivateThreadReplyView(ReplyView, PrivateThreadView):
    def get_state(
        self, request: HttpRequest, thread: Thread
    ) -> ReplyPrivateThreadState:
        return get_reply_private_thread_state(request, thread)

    def get_formset(
        self, request: HttpRequest, thread: Thread
    ) -> ReplyPrivateThreadFormset:
        return get_reply_private_thread_formset(request, thread)


thread_reply = ThreadReplyView.as_view()
private_thread_reply = PrivateThreadReplyView.as_view()
