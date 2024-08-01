from django.contrib import messages
from django.forms import ValidationError
from django.http import HttpRequest
from django.utils.translation import pgettext, pgettext_lazy

from ..categories.models import Category
from ..threads.models import Thread
from .forms import MoveThreads
from .results import ModerationResult, ModerationBulkResult, ModerationTemplateResult


class ThreadsBulkModerationAction:
    id: str
    name: str
    full_name: str | None
    submit_btn: str | None
    multistage: bool = False

    def __call__(
        self, request: HttpRequest, threads: list[Thread]
    ) -> ModerationResult | None:
        raise NotImplementedError()

    def get_context_data(self):
        return {
            "id": self.id,
            "name": str(self.name),
            "full_name": str(getattr(self, "full_name", self.name)),
            "submit_btn": str(getattr(self, "submit_btn", self.name)),
        }

    def create_bulk_result(self, threads: list[Thread]) -> ModerationBulkResult:
        return ModerationBulkResult(set(thread.id for thread in threads))


class MoveThreadsBulkModerationAction(ThreadsBulkModerationAction):
    id: str = "move"
    name: str = pgettext_lazy("threads bulk moderation action", "Move")
    full_name: str = pgettext_lazy("threads bulk moderation action", "Move threads")
    multistage: bool = True

    def __call__(self, request: HttpRequest, threads: list[Thread]) -> ModerationResult:
        if request.POST.get("confirm") == self.id:
            form = MoveThreads(
                request.POST,
                threads=threads,
                request=request,
            )

            if form.is_valid():
                category = Category.objects.get(id=form.cleaned_data["category"])
                result = self.execute(request, threads, category)
                if result.updated:
                    messages.success(
                        request,
                        pgettext("threads bulk open", "Threads moved"),
                    )

                return result
        else:
            form = MoveThreads(threads=threads, request=request)

        return ModerationTemplateResult(
            template_name="misago/moderation/move_threads.html",
            context={"form": form},
        )

    def execute(
        self, request: HttpRequest, threads: list[Thread], category: Category
    ) -> ModerationBulkResult | None:
        updated: list[Thread] = []
        for thread in threads:
            if thread.category_id != category.id:
                thread.move(category)
                thread.save()
                updated.append(thread)

        return self.create_bulk_result(updated)


class OpenThreadsBulkModerationAction(ThreadsBulkModerationAction):
    id: str = "open"
    name: str = pgettext_lazy("threads bulk moderation action", "Open")

    def __call__(
        self, request: HttpRequest, threads: list[Thread]
    ) -> ModerationBulkResult:
        closed_threads = [thread for thread in threads if thread.is_closed]
        updated = Thread.objects.filter(
            id__in=[thread.id for thread in closed_threads]
        ).update(is_closed=False)

        if updated:
            messages.success(
                request,
                pgettext("threads bulk open", "Threads opened"),
            )

        return self.create_bulk_result(closed_threads)


class CloseThreadsBulkModerationAction(ThreadsBulkModerationAction):
    id: str = "close"
    name: str = pgettext_lazy("threads bulk moderation action", "Close")

    def __call__(
        self, request: HttpRequest, threads: list[Thread]
    ) -> ModerationBulkResult:
        open_threads = [thread for thread in threads if not thread.is_closed]
        updated = Thread.objects.filter(
            id__in=[thread.id for thread in open_threads]
        ).update(is_closed=True)

        if updated:
            messages.success(
                request,
                pgettext("threads bulk open", "Threads closed"),
            )

        return self.create_bulk_result(open_threads)
