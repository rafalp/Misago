from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from ...core.exceptions import OutdatedSlug
from ..models import Thread
from .generic import PrivateThreadView, ThreadView


class RepliesView(View):
    template_name: str
    template_partial_name: str

    def get(
        self, request: HttpRequest, id: int, slug: str, page: int | None = None
    ) -> HttpResponse:
        thread = self.get_thread(request, id)

        if thread.slug != slug:
            raise OutdatedSlug(thread)

        context = self.get_context_data(request, thread, page)

        if request.is_htmx:
            template_name = self.template_partial_name
        else:
            template_name = self.template_name

        return render(request, template_name, context)

    def get_context_data(
        self, request: HttpRequest, thread: Thread, page: int | None = None
    ) -> dict:
        return {
            "thread": thread,
        }


class ThreadRepliesView(RepliesView, ThreadView):
    template_name: str = "misago/thread/index.html"
    template_partial_name: str = "misago/thread/replies.html"

    def get_context_data(
        self, request: HttpRequest, thread: Thread, page: int | None = None
    ) -> dict:
        context = super().get_context_data(request, thread, page)

        context.update(
            {
                "category": thread.category,
            }
        )

        return context


class PrivateThreadRepliesView(RepliesView, PrivateThreadView):
    template_name: str = "misago/private_thread/index.html"
    template_partial_name: str = "misago/private_thread/replies.html"


thread_replies = ThreadRepliesView.as_view()
private_thread_replies = PrivateThreadRepliesView.as_view()
