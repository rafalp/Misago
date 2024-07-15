from django.contrib import messages
from django.forms import ValidationError
from django.http import HttpRequest
from django.utils.translation import pgettext, pgettext_lazy

from ..threads.models import Thread
from .forms import MergeThreads


class ThreadsBulkModerationAction:
    id: str
    name: str
    full_name: str | None

    def __call__(
        self, request: HttpRequest, threads: list[Thread]
    ) -> dict | None:
        raise NotImplementedError()
    
    def get_context(self):
        return {
            "id": self.id,
            "name": str(self.name),
            "full_name": str(getattr(self, "full_name", self.name)),
        }


class MergeThreadsBulkModerationAction(ThreadsBulkModerationAction):
    id: str = "merge"
    name: str = pgettext_lazy("threads bulk moderation action", "Merge")
    full_name: str = pgettext_lazy("threads bulk moderation action", "Merge selected threads")

    def __call__(
        self, request: HttpRequest, threads: list[Thread]
    ) -> dict | None:
        if len(threads) < 2:
            raise ValidationError(
                pgettext(
                    "threads bulk merge",
                    "Select at least two threads to merge.",
                )
            )

        if request.POST.get("confirm") == "move":
            form = MergeThreads(
                request.POST,
                threads=threads,
                request=request,
            )

            if form.is_valid():
                pass
        else:
            form = MergeThreads(threads=threads, request=request)

        return {
            "form": form,
            "template_name": "misago/moderation/merge_threads.html",
        }


class OpenThreadsBulkModerationAction(ThreadsBulkModerationAction):
    id: str = "open"
    name: str = pgettext_lazy("threads bulk moderation action", "Open")

    def __call__(
        self, request: HttpRequest, threads: list[Thread]
    ) -> dict | None:
        closed_threads = [thread for thread in threads if thread.is_closed]
        updated = Thread.objects.filter(
            id__in=[thread.id for thread in closed_threads]
        ).update(is_closed=False)

        if updated:
            messages.success(
                request,
                pgettext("threads bulk open", "Threads opened"),
            )


class CloseThreadsBulkModerationAction(ThreadsBulkModerationAction):
    id: str = "close"
    name: str = pgettext_lazy("threads bulk moderation action", "Close")

    def __call__(
        self, request: HttpRequest, threads: list[Thread]
    ) -> dict | None:
        open_threads = [thread for thread in threads if not thread.is_closed]
        updated = Thread.objects.filter(
            id__in=[thread.id for thread in open_threads]
        ).update(is_closed=True)

        if updated:
            messages.success(
                request,
                pgettext("threads bulk open", "Threads closed"),
            )
