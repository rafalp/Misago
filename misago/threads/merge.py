from typing import Iterable

from django.db.models import Model
from django.forms import Form
from django.http import HttpRequest

from ..attachments.models import Attachment
from ..likes.models import Like
from ..notifications.models import Notification, WatchedThread
from ..polls.models import Poll, PollVote
from ..postedits.models import PostEdit
from ..postgres.delete import delete_all, delete_one
from ..readtracker.models import ReadThread
from ..threadupdates.models import ThreadUpdate
from .hooks import get_thread_merge_conflicts_hook
from .models import Post, Thread


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


def hook(action, *args, **kwargs):
    return action(*args, **kwargs)


def set_thread_merge_form_fields(
    form: Form, conflicts: dict[str, list[Model]], request: HttpRequest | None = None
):
    hook(_set_thread_merge_form_fields_action, form, conflicts, request)


def _set_thread_merge_form_fields_action(
    form: Form, conflicts: dict[str, list[Model]], request: HttpRequest | None = None
):
    pass


def get_thread_merge_form_conflict_resolutions(
    form: Form, conflicts: dict[str, list[Model]], request: HttpRequest | None = None
) -> dict[str, Model]:
    return hook(
        _get_thread_merge_form_conflict_resolutions_action, form, conflicts, request
    )


def _get_thread_merge_form_conflict_resolutions_action(
    form: Form, conflicts: dict[str, list[Model]], request: HttpRequest | None = None
) -> dict[str, Model]:
    pass


def merge_threads(
    new_thread: Thread,
    threads: Iterable[Thread],
    conflicts: dict[str, Model],
    request: HttpRequest | None = None,
) -> Thread:
    return hook(
        _merge_threads_action,
        new_thread,
        threads,
        conflicts,
        request,
    )


def _merge_threads_action(
    new_thread: Thread,
    threads: Iterable[Thread],
    conflicts: dict[str, Model],
    request: HttpRequest | None = None,
) -> Thread:
    new_category = new_thread.category

    poll = conflicts.get("poll")
    if poll and poll.thread_id != new_thread.id:
        if new_thread.has_poll:
            delete_all(PollVote, thread=new_thread)
            delete_all(Poll, thread=new_thread)

        poll.category = new_category
        poll.thread = new_thread
        poll.save()

        PollVote.objects.filter(poll=poll).update(
            thread=new_thread, category=new_category
        )

    solution = conflicts.get("solution")
    if solution and solution != new_thread:
        new_thread.solution_id = solution.solution_id
        new_thread.solution_posted_at = solution.solution_posted_at
        new_thread.solution_by_id = solution.solution_by_id
        new_thread.solution_by_name = solution.solution_by_name
        new_thread.solution_by_slug = solution.solution_by_slug
        new_thread.solution_selected_at = solution.solution_selected_at
        new_thread.solution_selected_by_id = solution.solution_selected_by_id
        new_thread.solution_selected_by_name = solution.solution_selected_by_name
        new_thread.solution_selected_by_slug = solution.solution_selected_by_slug

    for thread in threads:
        if thread == new_thread:
            continue

        Attachment.objects.filter(thread=thread).update(
            thread=new_thread, category=new_category
        )
        Like.objects.filter(thread=thread).update(
            thread=new_thread, category=new_category
        )
        Notification.objects.filter(thread=thread).update(
            thread=new_thread, category=new_category
        )
        Post.objects.filter(thread=thread).update(
            thread=new_thread, category=new_category
        )
        PostEdit.objects.filter(thread=thread).update(
            thread=new_thread, category=new_category
        )
        ThreadUpdate.objects.filter(thread=thread).update(
            thread=new_thread, category=new_category
        )
        WatchedThread.objects.filter(thread=thread).update(
            thread=new_thread, category=new_category
        )

        delete_all(PollVote, thread=thread)
        delete_all(Poll, thread=thread)
        delete_all(ReadThread, thread=thread)

        delete_one(thread)

        category = thread.category
        if category.last_thread_id == thread.id:
            category.last_thread = None
            category.save(update_fields=["last_thread"])

    new_thread.save()

    return new_thread
