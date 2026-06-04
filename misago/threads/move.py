from typing import Type

from django.db.models import Model
from django.http import HttpRequest

from ..attachments.models import Attachment
from ..categories.models import Category
from ..notifications.models import Notification, WatchedThread
from ..polls.models import Poll, PollVote
from ..readtracker.models import ReadThread
from ..threadupdates.models import ThreadUpdate
from .hooks import move_thread_hook
from .models import Post, Thread


def move_thread(
    thread: Thread,
    new_category: Category,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    return move_thread_hook(_move_thread_action, thread, new_category, commit, request)


def _move_thread_action(
    thread: Thread,
    new_category: Category,
    commit: bool = True,
    request: HttpRequest | None = None,
):
    if thread.category_id == new_category.id:
        return False

    thread.category = new_category

    _update_thread_relation(Attachment, thread, new_category)
    _update_thread_relation(Notification, thread, new_category)
    _update_thread_relation(Post, thread, new_category)
    _update_thread_relation(Poll, thread, new_category)
    _update_thread_relation(PollVote, thread, new_category)
    _update_thread_relation(ReadThread, thread, new_category)
    _update_thread_relation(ThreadUpdate, thread, new_category)
    _update_thread_relation(WatchedThread, thread, new_category)

    if commit:
        thread.save()

    return True


def _update_thread_relation(
    model: Type[Model],
    thread: Thread,
    new_category: Category,
):
    model.objects.filter(thread=thread).update(category=new_category)
