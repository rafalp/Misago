from django.contrib import messages
from django.forms import ValidationError
from django.http import HttpRequest
from django.utils.translation import pgettext, pgettext_lazy

from ..categories.models import Category
from ..threads.models import Thread
from .forms import MoveThreads


class ThreadsBulkModerationAction:
    id: str
    name: str
    full_name: str | None
    submit_btn: str | None

    def __call__(self, request: HttpRequest, threads: list[Thread]) -> dict | None:
        raise NotImplementedError()

    def get_context(self):
        return {
            "id": self.id,
            "name": str(self.name),
            "full_name": str(getattr(self, "full_name", self.name)),
            "submit_btn": str(getattr(self, "submit_btn", self.name)),
        }


class MoveThreadsBulkModerationAction(ThreadsBulkModerationAction):
    id: str = "move"
    name: str = pgettext_lazy("threads bulk moderation action", "Move")
    full_name: str = pgettext_lazy("threads bulk moderation action", "Move threads")

    def __call__(self, request: HttpRequest, threads: list[Thread]) -> dict | None:
        if request.POST.get("confirm") == "move":
            form = MoveThreads(
                request.POST,
                threads=threads,
                request=request,
            )

            if form.is_valid():
                category = Category.objects.get(id=form.cleaned_data["category"])
                if self.execute(request, threads, category):
                    messages.success(
                        request,
                        pgettext("threads bulk open", "Threads moved"),
                    )

                return
        else:
            form = MoveThreads(threads=threads, request=request)

        return {
            "form": form,
            "template_name": "misago/moderation/move_threads.html",
        }

    def execute(
        self, request: HttpRequest, threads: list[Thread], category: Category
    ) -> int:
        updated = 0
        for thread in threads:
            if thread.category_id != category.id:
                thread.move(category)
                thread.save()
                updated += 1

        return updated


class OpenThreadsBulkModerationAction(ThreadsBulkModerationAction):
    id: str = "open"
    name: str = pgettext_lazy("threads bulk moderation action", "Open")

    def __call__(self, request: HttpRequest, threads: list[Thread]) -> dict | None:
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

    def __call__(self, request: HttpRequest, threads: list[Thread]) -> dict | None:
        open_threads = [thread for thread in threads if not thread.is_closed]
        updated = Thread.objects.filter(
            id__in=[thread.id for thread in open_threads]
        ).update(is_closed=True)

        if updated:
            messages.success(
                request,
                pgettext("threads bulk open", "Threads closed"),
            )
