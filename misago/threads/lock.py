from typing import TYPE_CHECKING, Union

from django.http import HttpRequest
from django.utils import timezone

from ..core.utils import slugify
from .hooks import (
    lock_post_hook,
    lock_thread_hook,
    unlock_post_hook,
    unlock_thread_hook,
)
from .models import Post, Thread

if TYPE_CHECKING:
    from ..users.models import User


def lock_thread(
    thread: Thread,
    locked_by: Union["User", str, None] = None,
    lock_reason: str | None = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    return lock_thread_hook(
        _lock_thread_action, thread, locked_by, lock_reason, commit, request
    )


def _lock_thread_action(
    thread: Thread,
    locked_by: Union["User", str, None] = None,
    lock_reason: str | None = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    if thread.is_locked:
        return False

    thread.is_locked = True
    thread.locked_at = timezone.now()
    thread.lock_reason = lock_reason

    if isinstance(locked_by, str):
        thread.locked_by_name = locked_by
        thread.locked_by_slug = slugify(locked_by)
    elif locked_by:
        thread.locked_by = locked_by
        thread.locked_by_name = locked_by.username
        thread.locked_by_slug = locked_by.slug

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
    thread.locked_at = None
    thread.locked_by = None
    thread.locked_by_name = None
    thread.locked_by_slug = None
    thread.lock_reason = None

    if commit:
        thread.save()

    return True


def lock_post(
    post: Post,
    locked_by: Union["User", str] = None,
    lock_reason: str | None = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    return lock_post_hook(
        _lock_post_action, post, locked_by, lock_reason, commit, request
    )


def _lock_post_action(
    post: Post,
    locked_by: Union["User", str] = None,
    lock_reason: str | None = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    if post.is_locked:
        return False

    post.is_locked = True
    post.locked_at = timezone.now()
    post.lock_reason = lock_reason

    if isinstance(locked_by, str):
        post.locked_by_name = locked_by
        post.locked_by_slug = slugify(locked_by)
    elif locked_by:
        post.locked_by = locked_by
        post.locked_by_name = locked_by.username
        post.locked_by_slug = locked_by.slug

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
    post.locked_at = None
    post.locked_by = None
    post.locked_by_name = None
    post.locked_by_slug = None
    post.lock_reason = None

    if commit:
        post.save()

    return True
