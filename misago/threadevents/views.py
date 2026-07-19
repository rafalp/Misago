from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import pgettext, pgettext_lazy

from ..privatethreads.views.generic import PrivateThreadView
from ..threads.models import Thread
from ..threads.views.generic import ThreadView
from .delete import delete_thread_event
from .hide import hide_thread_event, unhide_thread_event
from .models import ThreadEvent
from .threadflag import sync_thread_has_events


class EventView:
    template_name: str = "misago/thread_events/event.html"
    success_message: str

    def post(
        self, request: HttpRequest, thread_id: int, slug: str, thread_event_id: int
    ) -> HttpResponse:
        if request.user.is_anonymous:
            self.raise_permission_error()

        thread = self.get_thread(request, thread_id)
        thread_event = self.get_thread_event(request, thread, thread_event_id)

        if not self.check_permission(request, thread):
            self.raise_permission_error()

        if self.execute_action(request, thread_event):
            messages.success(request, self.success_message)

        if not request.is_htmx:
            return redirect(self.get_next_thread_url(request, thread))

        thread_event.refresh_from_db()
        feed = self.get_post_feed(request, thread, [], [thread_event])
        feed.set_animated_thread_updates([thread_event.id])

        return render(
            request,
            self.template_name,
            {
                "thread_event": feed.get_feed_data()[0],
                "htmx_swap": True,
            },
        )

    def check_permission(self, request: HttpRequest, thread: Thread) -> bool:
        return False

    def execute_action(
        self, request: HttpRequest, thread_event: ThreadEvent
    ) -> ThreadEvent:
        return thread_event


class EventHideView(EventView):
    success_message = pgettext_lazy(
        "thread update hide success message", "Thread event hidden"
    )

    def execute_action(self, request: HttpRequest, thread_event: ThreadEvent) -> bool:
        return hide_thread_event(thread_event, request)

    def raise_permission_error(self):
        raise PermissionDenied(
            pgettext(
                "thread update hide permission error",
                "Only a moderator can hide thread events.",
            )
        )


class EventUnhideView(EventView):
    success_message = pgettext_lazy(
        "thread update unhide success message", "Thread event unhidden"
    )

    def execute_action(self, request: HttpRequest, thread_event: ThreadEvent) -> bool:
        return unhide_thread_event(thread_event, request)

    def raise_permission_error(self):
        raise PermissionDenied(
            pgettext(
                "thread update unhide permission error",
                "Only a moderator can unhide thread events.",
            )
        )


class ThreadEventHideView(EventHideView, ThreadView):
    def check_permission(self, request: HttpRequest, thread: Thread) -> bool:
        return request.user_permissions.is_category_moderator(thread.category_id)


class ThreadEventUnhideView(EventUnhideView, ThreadView):
    def check_permission(self, request: HttpRequest, thread: Thread) -> bool:
        return request.user_permissions.is_category_moderator(thread.category_id)


class PrivateThreadEventHideView(EventHideView, PrivateThreadView):
    def check_permission(self, request: HttpRequest, thread: Thread) -> bool:
        return request.user_permissions.is_private_threads_moderator


class PrivateThreadEventUnhideView(EventUnhideView, PrivateThreadView):
    def check_permission(self, request: HttpRequest, thread: Thread) -> bool:
        return request.user_permissions.is_private_threads_moderator


class EventDeleteView:
    thread_select_related = True
    thread_event_select_related = True

    template_name: str = "misago/thread_events/delete.html"
    confirm_template_name: str = "misago/thread_events/confirm_delete.html"
    success_message = pgettext_lazy("thread update deleted", "Thread event deleted")

    def post(
        self, request: HttpRequest, thread_id: int, slug: str, thread_event_id: int
    ) -> HttpResponse:
        if request.user.is_anonymous:
            self.raise_permission_error()

        thread = self.get_thread(request, thread_id)
        thread_event = self.get_thread_event(request, thread, thread_event_id)

        if not self.check_permission(request, thread):
            self.raise_permission_error()

        if request.is_htmx:
            self.execute_action(request, thread_event)
            return render(request, self.template_name)

        if request.POST.get("confirm"):
            self.execute_action(request, thread_event)
            return redirect(self.get_next_thread_url(request, thread))

        return render(
            request,
            self.confirm_template_name,
            {
                "thread": thread,
                "thread_event": thread_event,
                "next_url": self.get_next_thread_url(request, thread),
            },
        )

    def check_permission(self, request: HttpRequest, thread: Thread) -> bool:
        return False

    def raise_permission_error(self):
        raise PermissionDenied(
            pgettext(
                "thread update delete permission error",
                "Only a moderator can delete thread events.",
            )
        )

    def execute_action(self, request: HttpRequest, thread_event: ThreadEvent):
        thread = thread_event.thread

        delete_thread_event(thread_event, request)

        sync_thread_has_events(thread)

        messages.success(request, self.success_message)


class ThreadEventDeleteView(EventDeleteView, ThreadView):
    def check_permission(self, request: HttpRequest, thread: Thread) -> bool:
        return request.user_permissions.is_category_moderator(thread.category_id)


class PrivateThreadEventDeleteView(EventDeleteView, PrivateThreadView):
    def check_permission(self, request: HttpRequest, thread: Thread) -> bool:
        return request.user_permissions.is_private_threads_moderator
