from typing import Iterable

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import pgettext, pgettext_lazy

from ..privatethreads.views.backend import private_thread_backend
from ..threads.models import Thread
from ..threads.views.backend import thread_backend
from ..threads.views.generic import GenericThreadView
from .delete import delete_thread_event
from .hide import hide_thread_event, unhide_thread_event
from .models import ThreadEvent
from .threadeventtypes import (
    GenericThreadEventType,
    private_thread_event_type,
    thread_event_type,
)
from .threadflag import sync_thread_has_events


class EventView(GenericThreadView):
    thread_event_type: GenericThreadEventType

    def get_thread_event_queryset(
        self,
        request: HttpRequest,
        thread: Thread,
    ) -> QuerySet:
        return self.thread_event_type.get_thread_event_queryset(request, thread)

    def get_thread_event(
        self,
        request: HttpRequest,
        thread: Thread,
        thread_event_id: int,
        *,
        select_related: bool | Iterable[str] = False,
    ) -> ThreadEvent:
        return self.thread_event_type.get_thread_event(
            request, thread, thread_event_id, select_related=select_related
        )


class EventVisibilityView(EventView):
    template_name: str = "misago/thread_events/event.html"
    success_message: str

    def post(
        self, request: HttpRequest, thread_id: int, slug: str, thread_event_id: int
    ) -> HttpResponse:
        if request.user.is_anonymous:
            self.raise_permission_error()

        thread = self.get_thread(request, thread_id)
        thread_event = self.get_thread_event(request, thread, thread_event_id)

        if not self.has_moderator_permission(request.user_permissions, thread):
            self.raise_permission_error()

        if self.perform_action(request, thread_event):
            messages.success(request, self.success_message)

        if not request.is_htmx:
            return redirect(self.get_next_thread_url(request, thread))

        thread_event.refresh_from_db()
        feed = self.get_post_feed(request, thread, [], [thread_event])
        feed.set_animated_thread_events([thread_event.id])

        return render(
            request,
            self.template_name,
            {
                "thread_event": feed.get_feed_data()[0],
                "htmx_swap": True,
            },
        )

    def perform_action(
        self, request: HttpRequest, thread_event: ThreadEvent
    ) -> ThreadEvent:
        return thread_event


class EventHideView(EventVisibilityView):
    success_message = pgettext_lazy(
        "thread update hide success message", "Thread event hidden"
    )

    def perform_action(self, request: HttpRequest, thread_event: ThreadEvent) -> bool:
        return hide_thread_event(thread_event, request)

    def raise_permission_error(self):
        raise PermissionDenied(
            pgettext(
                "thread update hide permission error",
                "Only a moderator can hide thread events.",
            )
        )


class EventUnhideView(EventVisibilityView):
    success_message = pgettext_lazy(
        "thread update unhide success message", "Thread event unhidden"
    )

    def perform_action(self, request: HttpRequest, thread_event: ThreadEvent) -> bool:
        return unhide_thread_event(thread_event, request)

    def raise_permission_error(self):
        raise PermissionDenied(
            pgettext(
                "thread update unhide permission error",
                "Only a moderator can unhide thread events.",
            )
        )


class ThreadEventHideView(EventHideView):
    backend = thread_backend
    thread_event_type = thread_event_type


class ThreadEventUnhideView(EventUnhideView):
    backend = thread_backend
    thread_event_type = thread_event_type


class PrivateThreadEventHideView(EventHideView):
    backend = private_thread_backend
    thread_event_type = private_thread_event_type


class PrivateThreadEventUnhideView(EventUnhideView):
    backend = private_thread_backend
    thread_event_type = private_thread_event_type


class EventDeleteView(EventView):
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

        if not self.has_moderator_permission(request.user_permissions, thread):
            self.raise_permission_error()

        if request.is_htmx:
            self.perform_action(request, thread_event)
            return render(request, self.template_name)

        if request.POST.get("confirm"):
            self.perform_action(request, thread_event)
            return redirect(self.get_next_thread_url(request, thread))

        return render(
            request, self.confirm_template_name, self.get_context_data(thread_event)
        )

    def get_thread(self, request: Thread, thread_id: int, **kwargs) -> Thread:
        return super().get_thread(request, thread_id, select_related=True)

    def raise_permission_error(self):
        raise PermissionDenied(
            pgettext(
                "thread update delete permission error",
                "Only a moderator can delete thread events.",
            )
        )

    def get_context_data(self, thread_event: Thread) -> dict:
        thread = thread_event.thread

        return {
            "breadcrumbs": self.get_thread_breadcrumbs(self.request, thread),
            "thread": thread,
            "thread_event": thread_event,
            "next_url": self.get_next_thread_url(self.request, thread),
        }

    def perform_action(self, request: HttpRequest, thread_event: ThreadEvent):
        thread = thread_event.thread

        delete_thread_event(thread_event, request)
        sync_thread_has_events(thread)

        messages.success(request, self.success_message)


class ThreadEventDeleteView(EventDeleteView):
    backend = thread_backend
    thread_event_type = thread_event_type


class PrivateThreadEventDeleteView(EventDeleteView):
    backend = private_thread_backend
    thread_event_type = private_thread_event_type
