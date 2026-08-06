from abc import ABC
from typing import Iterable

from django.db.models import QuerySet
from django.http import Http404, HttpRequest

from ..permissions.privatethreads import filter_private_thread_updates_queryset
from ..permissions.threads import filter_thread_updates_queryset
from ..threads.models import Thread
from .models import ThreadEvent


class BaseThreadEventType(ABC):
    def get_thread_event_queryset(
        self,
        request: HttpRequest,
        thread: Thread,
    ) -> QuerySet:
        return ThreadEvent.objects.filter(thread=thread).order_by("-id")

    def get_thread_event(
        self,
        request: HttpRequest,
        thread: Thread,
        thread_event_id: int,
        *,
        select_related: bool | Iterable[str] = False,
    ) -> ThreadEvent:
        queryset = self.get_thread_event_queryset(request, thread)
        if select_related is True:
            queryset = queryset.select_related()
        elif select_related:
            queryset = queryset.select_related(*select_related)

        try:
            thread_event = queryset.get(id=thread_event_id)
        except ThreadEvent.DoesNotExist:
            raise Http404()

        if Thread.category.is_cached(thread):
            thread_event.category = thread.category

        thread_event.thread = thread

        return thread_event


class ThreadEventType(BaseThreadEventType):
    def get_thread_event_queryset(
        self,
        request: HttpRequest,
        thread: Thread,
    ) -> QuerySet:
        return filter_thread_updates_queryset(
            request.user_permissions,
            thread,
            super().get_thread_event_queryset(request, thread),
        )


class PrivateThreadEventType(BaseThreadEventType):
    def get_thread_event_queryset(
        self,
        request: HttpRequest,
        thread: Thread,
    ) -> QuerySet:
        return filter_private_thread_updates_queryset(
            request.user_permissions,
            thread,
            super().get_thread_event_queryset(request, thread),
        )


thread_event_type = ThreadEventType()
private_thread_event_type = PrivateThreadEventType()
