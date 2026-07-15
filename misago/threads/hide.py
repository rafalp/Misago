from typing import TYPE_CHECKING, Union

from django.http import HttpRequest
from django.utils import timezone

from ..core.utils import slugify
from .hooks import (
    hide_post_hook,
    hide_thread_hook,
    unhide_post_hook,
    unhide_thread_hook,
)
from .models import Post, Thread

if TYPE_CHECKING:
    from ..users.models import User


def hide_thread(
    thread: Thread,
    hidden_by: Union["User", str],
    hide_reason: str | None = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    return hide_thread_hook(
        _hide_thread_action, thread, hidden_by, hide_reason, commit, request
    )


def _hide_thread_action(
    thread: Thread,
    hidden_by: Union["User", str],
    hide_reason: str | None = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    if thread.is_hidden:
        return False

    thread.is_hidden = True
    thread.hidden_at = timezone.now()
    thread.hide_reason = hide_reason

    if isinstance(hidden_by, str):
        thread.hidden_by_name = hidden_by
        thread.hidden_by_slug = slugify(hidden_by)
    else:
        thread.hidden_by = hidden_by
        thread.hidden_by_name = hidden_by.username
        thread.hidden_by_slug = hidden_by.slug

    if commit:
        thread.save()

    return True


def unhide_thread(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    return unhide_thread_hook(_unhide_thread_action, thread, commit, request)


def _unhide_thread_action(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    if not thread.is_hidden:
        return False

    thread.is_hidden = False
    thread.hidden_at = None
    thread.hidden_by = None
    thread.hidden_by_name = None
    thread.hidden_by_slug = None
    thread.hide_reason = None

    if commit:
        thread.save()

    return True


def hide_post(
    post: Post,
    hidden_by: Union["User", str],
    hide_reason: str | None = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    return hide_post_hook(
        _hide_post_action, post, hidden_by, hide_reason, commit, request
    )


def _hide_post_action(
    post: Post,
    hidden_by: Union["User", str],
    hide_reason: str | None = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    if post.is_hidden:
        return False

    post.is_hidden = True
    post.hidden_at = timezone.now()
    post.hide_reason = hide_reason

    if isinstance(hidden_by, str):
        post.hidden_by_name = hidden_by
        post.hidden_by_slug = slugify(hidden_by)
    else:
        post.hidden_by = hidden_by
        post.hidden_by_name = hidden_by.username
        post.hidden_by_slug = hidden_by.slug

    if commit:
        post.save()

    return True


def unhide_post(
    post: Post, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    return unhide_post_hook(_unhide_post_action, post, commit, request)


def _unhide_post_action(
    post: Post, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    if not post.is_hidden:
        return False

    post.is_hidden = False
    post.hidden_at = None
    post.hidden_by = None
    post.hidden_by_name = None
    post.hidden_by_slug = None
    post.hide_reason = None

    if commit:
        post.save()

    return True
