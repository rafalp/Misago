from typing import Iterable

from django.db.models import Model
from django.http import HttpRequest

from ..polls.models import Poll
from .hooks import get_thread_merge_conflicts_hook
from .models import Thread


def get_thread_merge_conflicts(
    threads: Iterable[Thread], request: HttpRequest | None = None
) -> dict[str, list[Model]]:
    return get_thread_merge_conflicts_hook(
        _get_thread_merge_conflicts_action, threads, request
    )


def _get_thread_merge_conflicts_action(
    threads: Iterable[Thread], request: HttpRequest | None = None
) -> dict[str, list[Model]]:
    threads_dict = {thread.id: thread for thread in threads}
    conflicts = {}

    if polls := list(Poll.objects.filter(thread__in=threads).order_by("thread")):
        for poll in polls:
            poll.thread = threads_dict[poll.thread_id]
            poll.category = poll.thread.category

        conflicts["poll"] = polls

    if solution := [thread for thread in threads if thread.solution_id]:
        conflicts["solution"] = sorted(solution, key=lambda t: t.id)

    return conflicts
