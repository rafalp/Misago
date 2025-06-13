from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import pgettext, pgettext_lazy

from ..models import Thread, ThreadUpdate
from ..threadupdates import hide_thread_update, unhide_thread_update
from .generic import PrivateThreadView, ThreadView


class ThreadUpdateView:
    template_name: str
    template_name_htmx: str
    success_message: str

    def post(
        self, request: HttpRequest, id: int, slug: str, thread_update_id: id
    ) -> HttpResponse:
        thread = self.get_thread(request, id)
        thread_update = self.get_thread_update(request, thread, thread_update_id)

        if self.execute_action(request, thread_update):
            messages.success(request, self.success_message)

        if request.is_htmx:
            feed = self.get_posts_feed(request, thread, [], [thread_update])
            return render(request, self.template_name, {"feed": feed})

        return redirect(self.clean_thread_url(thread, request.POST.get("next")))

    def execute_action(
        self, request: HttpRequest, thread_update: ThreadUpdate
    ) -> ThreadUpdate:
        return thread_update


class HideThreadUpdateMixin:
    success_message = pgettext_lazy("thread update hidden", "Thread update hidden")

    def execute_action(self, request: HttpRequest, thread_update: ThreadUpdate) -> bool:
        return hide_thread_update(thread_update, request)


class UnhideThreadUpdateMixin:
    success_message = pgettext_lazy("thread update unhidden", "Thread update unhidden")

    def execute_action(self, request: HttpRequest, thread_update: ThreadUpdate) -> bool:
        return unhide_thread_update(thread_update, request)


class HideThreadUpdateView(HideThreadUpdateMixin, ThreadUpdateView, ThreadView):
    pass


class HidePrivateThreadView(HideThreadUpdateMixin, ThreadUpdateView, PrivateThreadView):
    pass


class UnhideThreadUpdateView(UnhideThreadUpdateMixin, ThreadUpdateView, ThreadView):
    pass


class UnhidePrivateThreadUpdateView(
    UnhideThreadUpdateMixin, ThreadUpdateView, PrivateThreadView
):
    pass


hide_thread_update_view = HideThreadUpdateView.as_view()
hide_private_thread_update_view = HidePrivateThreadView.as_view()

unhide_thread_update_view = UnhideThreadUpdateView.as_view()
unhide_private_thread_update_view = UnhidePrivateThreadUpdateView.as_view()
