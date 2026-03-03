from typing import TYPE_CHECKING, Union

from django.http import HttpRequest
from django.utils import timezone

from ..threads.models import Post, Thread
from .hooks import clear_thread_solution_hook, set_thread_solution_hook

if TYPE_CHECKING:
    from ..users.models import User


def set_thread_solution(
    thread: Thread,
    post: Post,
    user: Union["User", str],
    commit: bool = True,
    request: HttpRequest | None = None,
):
    set_thread_solution_hook(
        _set_thread_solution_action, thread, post, user, commit, request
    )


def _set_thread_solution_action(
    thread: Thread,
    post: Post,
    user: Union["User", str],
    commit: bool = True,
    request: HttpRequest | None = None,
):
    thread.solution = post
    thread.solution_by = post.poster
    thread.solution_by_name = post.poster_name
    thread.solution_by_slug = post.poster_slug
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
