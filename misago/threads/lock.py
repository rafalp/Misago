from django.http import HttpRequest

from .hooks import (
    lock_post_hook,
    lock_thread_hook,
    unlock_post_hook,
    unlock_thread_hook,
)
from .models import Post, Thread


def lock_thread(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    return lock_thread_hook(_lock_thread_action, thread, commit, request)


def _lock_thread_action(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    if thread.is_locked:
        return False

    thread.is_locked = True

    if commit:
        thread.save()

    return True


def unlock_thread(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    return unlock_thread_hook(_unlock_thread_action, thread, commit, request)


def _unlock_thread_action(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    if not thread.is_locked:
        return False

    thread.is_locked = False

    if commit:
        thread.save()

    return True


def lock_post(
    post: Post, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    return lock_post_hook(_lock_post_action, post, commit, request)


def _lock_post_action(
    post: Post, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    if post.is_locked:
        return False

    post.is_locked = True

    if commit:
        post.save()

    return True


def unlock_post(
    post: Post, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    return unlock_post_hook(_unlock_post_action, post, commit, request)


def _unlock_post_action(
    post: Post, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    if not post.is_locked:
        return False

    post.is_locked = False

    if commit:
        post.save()

    return True
