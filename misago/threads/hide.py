from typing import TYPE_CHECKING, Union

from django.http import HttpRequest
from django.utils import timezone

from ..core.utils import slugify
from .hooks import hide_thread_hook, unhide_thread_hook
from .models import Thread

if TYPE_CHECKING:
    from ..users.models import User


def hide_thread(
    thread: Thread,
    hidden_by: Union["User", str],
    hidden_reason: str | None = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    return hide_thread_hook(
        _hide_thread_action, thread, hidden_by, hidden_reason, commit, request
    )


def _hide_thread_action(
    thread: Thread,
    hidden_by: Union["User", str],
    hidden_reason: str | None = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    if thread.is_hidden:
        return False

    thread.is_hidden = True
    thread.hidden_at = timezone.now()
    thread.hidden_reason = hidden_reason

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
    thread.hidden_reason = None

    if commit:
        thread.save()

    return True
