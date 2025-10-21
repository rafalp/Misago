from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import pgettext, pgettext_lazy

from ..privatethreads.views.generic import PrivateThreadView
from ..threads.models import Thread
from ..threads.views.generic import ThreadView
from .delete import delete_thread_update
from .hide import hide_thread_update, unhide_thread_update
from .models import ThreadUpdate


class UpdateView:
    template_name: str = "misago/thread_update/update.html"
    success_message: str

    def post(
        self, request: HttpRequest, thread_id: int, slug: str, thread_update_id: int
    ) -> HttpResponse:
        if request.user.is_anonymous:
            self.raise_permission_error()

        thread = self.get_thread(request, thread_id)
        thread_update = self.get_thread_update(request, thread, thread_update_id)

        if not self.check_permission(request, thread):
            self.raise_permission_error()

        if self.execute_action(request, thread_update):
            messages.success(request, self.success_message)

        if not request.is_htmx:
            return redirect(self.get_next_thread_url(request, thread))

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


class UpdateHideView(UpdateView):
    success_message = pgettext_lazy(
        "thread update hide success message", "Thread update hidden"
    )

    def execute_action(self, request: HttpRequest, thread_update: ThreadUpdate) -> bool:
        return hide_thread_update(thread_update, request)

    def raise_permission_error(self):
        raise PermissionDenied(
            pgettext(
                "thread update hide permission error",
                "Only a moderator can hide thread updates.",
            )
        )


class UpdateUnhideView(UpdateView):
    success_message = pgettext_lazy(
        "thread update unhide success message", "Thread update unhidden"
    )

    def execute_action(self, request: HttpRequest, thread_update: ThreadUpdate) -> bool:
        return unhide_thread_update(thread_update, request)

    def raise_permission_error(self):
        raise PermissionDenied(
            pgettext(
                "thread update unhide permission error",
                "Only a moderator can unhide thread updates.",
            )
        )


class ThreadUpdateHideView(UpdateHideView, ThreadView):
    def check_permission(self, request: HttpRequest, thread: Thread) -> bool:
        return request.user_permissions.is_category_moderator(thread.category_id)


class ThreadUpdateUnhideView(UpdateUnhideView, ThreadView):
    def check_permission(self, request: HttpRequest, thread: Thread) -> bool:
        return request.user_permissions.is_category_moderator(thread.category_id)


class PrivateThreadUpdateHideView(UpdateHideView, PrivateThreadView):
    def check_permission(self, request: HttpRequest, thread: Thread) -> bool:
        return request.user_permissions.is_private_threads_moderator


class PrivateThreadUpdateUnhideView(UpdateUnhideView, PrivateThreadView):
    def check_permission(self, request: HttpRequest, thread: Thread) -> bool:
        return request.user_permissions.is_private_threads_moderator


class UpdateDeleteView:
    thread_select_related = True
    thread_update_select_related = True

    template_name: str = "misago/thread_update/delete.html"
    confirm_template_name: str = "misago/thread_update/confirm_delete.html"
    success_message = pgettext_lazy("thread update deleted", "Thread update deleted")

    def post(
        self, request: HttpRequest, thread_id: int, slug: str, thread_update_id: int
    ) -> HttpResponse:
        if request.user.is_anonymous:
            self.raise_permission_error()

        thread = self.get_thread(request, thread_id)
        thread_update = self.get_thread_update(request, thread, thread_update_id)

        if not self.check_permission(request, thread):
            self.raise_permission_error()

        if request.is_htmx:
            self.execute_action(request, thread_update)
            return render(request, self.template_name)

        if request.POST.get("confirm"):
            self.execute_action(request, thread_update)
            return redirect(self.get_next_thread_url(request, thread))

        return render(
            request,
            self.confirm_template_name,
            {
                "thread": thread,
                "thread_update": thread_update,
                "next_url": self.get_next_thread_url(request, thread),
            },
        )

    def check_permission(self, request: HttpRequest, thread: Thread) -> bool:
        return False

    def raise_permission_error(self):
        raise PermissionDenied(
            pgettext(
                "thread update delete permission error",
                "Only a moderator can delete thread updates.",
            )
        )

    def execute_action(self, request: HttpRequest, thread_update: ThreadUpdate):
        delete_thread_update(thread_update, request)
        messages.success(request, self.success_message)


class ThreadUpdateDeleteView(UpdateDeleteView, ThreadView):
    def check_permission(self, request: HttpRequest, thread: Thread) -> bool:
        return request.user_permissions.is_category_moderator(thread.category_id)


class PrivateThreadUpdateDeleteView(UpdateDeleteView, PrivateThreadView):
    def check_permission(self, request: HttpRequest, thread: Thread) -> bool:
        return request.user_permissions.is_private_threads_moderator
