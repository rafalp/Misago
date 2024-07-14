from django.http import HttpRequest, HttpResponse
from django.utils.translation import pgettext_lazy

from ..categories.models import Category
from ..threads.models import Thread


class ThreadsBulkModerationAction:
    id: str
    name: str

    def __call__(self, request: HttpRequest, threads: list[Thread]) -> HttpResponse | None:
        raise NotImplementedError()


class OpenThreadsBulkModerationAction(ThreadsBulkModerationAction):
    id: str = "open"
    name: str = pgettext_lazy("threads bulk moderation action", "Open threads")

    def __call__(self, request: HttpRequest, threads: list[Thread]) -> HttpResponse | None:
        closed_threads = [thread for thread in threads if thread.is_closed]
        updated = Thread.objects.filter(
            id__in=[thread.id for thread in closed_threads]
        ).update(is_closed=False)


class CloseThreadsBulkModerationAction(ThreadsBulkModerationAction):
    id: str = "close"
    name: str = pgettext_lazy("threads bulk moderation action", "Close threads")

    def __call__(self, request: HttpRequest, threads: list[Thread]) -> HttpResponse | None:
        open_threads = [thread for thread in threads if not thread.is_closed]
        updated = Thread.objects.filter(
            id__in=[thread.id for thread in open_threads]
        ).update(is_closed=True)
