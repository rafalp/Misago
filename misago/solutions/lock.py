from typing import TYPE_CHECKING, Union

from django.http import HttpRequest
from django.utils import timezone

from ..threads.models import Thread
from .hooks import (
    lock_thread_solution_hook,
    unlock_thread_solution_hook,
)

if TYPE_CHECKING:
    from ..users.models import User


def lock_thread_solution(
    thread: Thread,
    user: Union["User", str],
    commit: bool = True,
    request: HttpRequest | None = None,
):
    lock_thread_solution_hook(
        _lock_thread_solution_action, thread, user, commit, request
    )


def _lock_thread_solution_action(
    thread: Thread,
    user: Union["User", str],
    commit: bool = True,
    request: HttpRequest | None = None,
):
    if isinstance(user, str):
        locked_by = None
        locked_by_name = user
        locked_by_slug = None
    else:
        locked_by = user
        locked_by_name = user.username
        locked_by_slug = user.slug

    thread.solution_is_locked = True
    thread.solution_locked_at = timezone.now()
    thread.solution_locked_by = locked_by
    thread.solution_locked_by_name = locked_by_name
    thread.solution_locked_by_slug = locked_by_slug

    if commit:
        thread.save()


def unlock_thread_solution(
    thread: Thread,
    commit: bool = True,
    request: HttpRequest | None = None,
):
    unlock_thread_solution_hook(_unlock_thread_solution_action, thread, commit, request)


def _unlock_thread_solution_action(
    thread: Thread,
    commit: bool = True,
    request: HttpRequest | None = None,
):
    thread.solution_is_locked = False
    thread.solution_locked_at = None
    thread.solution_locked_by = None
    thread.solution_locked_by_name = None
    thread.solution_locked_by_slug = None

    if commit:
        thread.save()
