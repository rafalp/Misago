from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import pgettext, pgettext_lazy

from ..models import Thread, ThreadUpdate
from ..threadupdates import (
    delete_thread_update,
    hide_thread_update,
    unhide_thread_update,
)
from .generic import PrivateThreadView, ThreadView


class BaseUpdateView:
    template_name: str = "misago/thread_update/update.html"
    success_message: str

    def post(
        self, request: HttpRequest, id: int, slug: str, thread_update_id: id
    ) -> HttpResponse:
        thread = self.get_thread(request, id)
        thread_update = self.get_thread_update(request, thread, thread_update_id)

        if not self.check_permission(request, thread):
            self.raise_permission_error()

        if self.execute_action(request, thread_update):
            messages.success(request, self.success_message)

        if not request.is_htmx:
            return redirect(self.clean_thread_url(thread, request.POST.get("next")))

        thread_update.refresh_from_db()
        feed = self.get_posts_feed(request, thread, [], [thread_update])
        feed.set_animated_thread_updates([thread_update.id])

        return render(
            request,
            self.template_name,
            {
                "thread_update": feed.get_feed_data()[0],
                "htmx_swap": True,
            },
        )

    def check_permission(self, request: HttpRequest, thread: Thread) -> bool:
        return False

    def execute_action(
        self, request: HttpRequest, thread_update: ThreadUpdate
    ) -> ThreadUpdate:
        return thread_update


class HideThreadUpdateMixin:
    success_message = pgettext_lazy("thread update hidden", "Thread update hidden")

    def execute_action(self, request: HttpRequest, thread_update: ThreadUpdate) -> bool:
        return hide_thread_update(thread_update, request)

    def raise_permission_error(self):
        raise PermissionDenied(
            pgettext(
                "hide thread update error", "Only a moderator can hide thread updates."
            )
        )


class UnhideThreadUpdateMixin:
    success_message = pgettext_lazy("thread update unhidden", "Thread update unhidden")

    def execute_action(self, request: HttpRequest, thread_update: ThreadUpdate) -> bool:
        return unhide_thread_update(thread_update, request)

    def raise_permission_error(self):
        raise PermissionDenied(
            pgettext(
                "hide thread update error",
                "Only a moderator can unhide thread updates.",
            )
        )


class HideThreadUpdateView(HideThreadUpdateMixin, BaseUpdateView, ThreadView):
    def check_permission(self, request: HttpRequest, thread: Thread) -> bool:
        return request.user_permissions.is_category_moderator(thread.category_id)


class UnhideThreadUpdateView(UnhideThreadUpdateMixin, BaseUpdateView, ThreadView):
    def check_permission(self, request: HttpRequest, thread: Thread) -> bool:
        return request.user_permissions.is_category_moderator(thread.category_id)


class HidePrivateThreadView(HideThreadUpdateMixin, BaseUpdateView, PrivateThreadView):
    def check_permission(self, request: HttpRequest, thread: Thread) -> bool:
        return request.user_permissions.is_private_threads_moderator


class UnhidePrivateThreadUpdateView(
    UnhideThreadUpdateMixin, BaseUpdateView, PrivateThreadView
):
    def check_permission(self, request: HttpRequest, thread: Thread) -> bool:
        return request.user_permissions.is_private_threads_moderator


class DeleteUpdateView:
    success_message = pgettext_lazy("thread update deleted", "Thread update deleted")

    def post(
        self, request: HttpRequest, id: int, slug: str, thread_update_id: id
    ) -> HttpResponse:
        thread = self.get_thread(request, id)
        thread_update = self.get_thread_update(request, thread, thread_update_id)

        if not self.check_permission(request, thread):
            self.raise_permission_error()

        delete_thread_update(thread_update, request)
        messages.success(request, self.success_message)

        if request.is_htmx:
            feed = self.get_posts_feed(request, thread, [], [thread_update])
            return render(request, self.template_name, {"feed": feed})

        return redirect(self.clean_thread_url(thread, request.POST.get("next")))

    def check_permission(self, request: HttpRequest, thread: Thread) -> bool:
        return False

    def raise_permission_error(self):
        raise PermissionDenied(
            pgettext(
                "delete thread update error",
                "Only a moderator can delete thread updates.",
            )
        )


class DeleteThreadUpdateView(DeleteUpdateView, ThreadView):
    def check_permission(self, request: HttpRequest, thread: Thread) -> bool:
        return request.user_permissions.is_category_moderator(thread.category_id)


class DeletePrivateThreadView(DeleteUpdateView, PrivateThreadView):
    def check_permission(self, request: HttpRequest, thread: Thread) -> bool:
        return request.user_permissions.is_private_threads_moderator


hide_thread_update_view = HideThreadUpdateView.as_view()
hide_private_thread_update_view = HidePrivateThreadView.as_view()

unhide_thread_update_view = UnhideThreadUpdateView.as_view()
unhide_private_thread_update_view = UnhidePrivateThreadUpdateView.as_view()

delete_thread_update_view = DeleteThreadUpdateView.as_view()
delete_private_thread_update_view = DeletePrivateThreadView.as_view()
