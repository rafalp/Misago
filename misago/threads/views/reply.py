from django.http import HttpRequest, HttpResponse
from django.views import View

from ...posting.forms import PostingFormset
from ...posting.state import ReplyPrivateThreadState, ReplyThreadState
from ..models import Thread
from .generic import PrivateThreadView, ThreadView


class ReplyView(View):
    def get(self, request: HttpRequest, id: int, slug: str) -> HttpResponse:
        thread = self.get_thread(request, id)
        formset = self.get_formset(request, thread)

    def post(self, request: HttpRequest, id: int, slug: str) -> HttpResponse:
        thread = self.get_thread(request, id)
        state = self.get_state(request, thread)
        formset = self.get_formset(request, thread)

    def get_state(self, request: HttpRequest, thread: Thread) -> ReplyThreadState:
        raise NotImplementedError()

    def get_formset(self, request: HttpRequest, thread: Thread) -> PostingFormset:
        raise NotImplementedError()


class ThreadReplyView(ReplyView, ThreadView):
    def get_state(self, request: HttpRequest, thread: Thread) -> ReplyThreadState:
        raise NotImplementedError()

    def get_formset(self, request: HttpRequest, thread: Thread) -> PostingFormset:
        raise NotImplementedError()


class PrivateThreadReplyView(ReplyView, PrivateThreadView):
    def get_state(
        self, request: HttpRequest, thread: Thread
    ) -> ReplyPrivateThreadState:
        raise NotImplementedError()

    def get_formset(self, request: HttpRequest, thread: Thread) -> PostingFormset:
        raise NotImplementedError()


thread_reply = ThreadReplyView.as_view()
private_thread_reply = PrivateThreadReplyView.as_view()
