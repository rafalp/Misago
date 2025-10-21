from typing import Iterable, Type

from django.http import HttpRequest
from django.db.models import Model

from ..attachments.models import Attachment
from ..categories.models import Category
from ..notifications.models import Notification, WatchedThread
from ..polls.models import Poll, PollVote
from ..readtracker.models import ReadThread
from ..threadupdates.models import ThreadUpdate
from .hooks import move_threads_hook
from .models import Post, Thread


def move_threads(
    threads: Iterable[Thread] | Thread,
    new_category: Category,
    commit: bool = True,
    request: HttpRequest | None = None,
):
    if isinstance(threads, Thread):
        threads = [threads]

    move_threads_hook(_move_threads_action, threads, new_category, commit, request)


def _move_threads_action(
    threads: Iterable[Thread],
    new_category: Category,
    commit: bool = True,
    request: HttpRequest | None = None,
):
    for thread in threads:
        thread.category = new_category

    if commit:
        # We skip loop with `thread.save` for performance reasons
        Thread.objects.filter(
            id__in=[thread.id for thread in threads],
        ).update(category=new_category)

    _update_threads_relations(Attachment, threads, new_category)
    _update_threads_relations(Notification, threads, new_category)
    _update_threads_relations(Post, threads, new_category)
    _update_threads_relations(Poll, threads, new_category)
    _update_threads_relations(PollVote, threads, new_category)
    _update_threads_relations(ReadThread, threads, new_category)
    _update_threads_relations(ThreadUpdate, threads, new_category)
    _update_threads_relations(WatchedThread, threads, new_category)


def _update_threads_relations(
    model: Type[Model],
    threads: Iterable[Thread],
    new_category: Category,
):
    model.objects.filter(thread__in=threads).update(category=new_category)
