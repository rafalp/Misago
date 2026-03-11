from typing import TYPE_CHECKING, Union

from django.http import HttpRequest
from django.utils import timezone

from ..threads.models import Post, Thread
from .hooks import (
    clear_thread_solution_hook,
    lock_thread_solution_hook,
    select_thread_solution_hook,
    unlock_thread_solution_hook,
)

if TYPE_CHECKING:
    from ..users.models import User


def select_thread_solution(
    thread: Thread,
    post: Post,
    user: Union["User", str],
    commit: bool = True,
    request: HttpRequest | None = None,
):
    select_thread_solution_hook(
        _select_thread_solution_action, thread, post, user, commit, request
    )


def _select_thread_solution_action(
    thread: Thread,
    post: Post,
    user: Union["User", str],
    commit: bool = True,
    request: HttpRequest | None = None,
):
    thread.solution = post

    if post.poster:
        thread.solution_by = post.poster
        thread.solution_by_name = post.poster.username
        thread.solution_by_slug = post.poster.slug
    else:
        thread.solution_by_name = post.poster_name

    thread.solution_selected_at = timezone.now()

    if isinstance(user, str):
        selected_by = None
        selected_by_name = user
        selected_by_slug = None
    else:
        selected_by = user
        selected_by_name = user.username
        selected_by_slug = user.slug

    thread.solution_selected_by = selected_by
    thread.solution_selected_by_name = selected_by_name
    thread.solution_selected_by_slug = selected_by_slug

    if commit:
        thread.save()


def clear_thread_solution(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
):
    clear_thread_solution_hook(_clear_thread_solution_action, thread, commit, request)


def _clear_thread_solution_action(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
):
    thread.solution = None
    thread.solution_by = None
    thread.solution_by_name = None
    thread.solution_by_slug = None
    thread.solution_selected_at = None
    thread.solution_selected_by = None
    thread.solution_selected_by_name = None
    thread.solution_selected_by_slug = None

    if commit:
        thread.save()


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
