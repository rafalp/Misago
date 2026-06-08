from django.http import HttpRequest

from .hooks import (
    approve_thread_hook,
    remove_thread_reply_approval_hook,
    require_thread_reply_approval_hook,
)
from .models import Thread


def approve_thread(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    return approve_thread_hook(_approve_thread_action, thread, commit, request)


def _approve_thread_action(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    if not thread.is_unapproved:
        return False

    thread.is_unapproved = False

    if commit:
        thread.save()

    return True


def require_thread_reply_approval(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    return require_thread_reply_approval_hook(
        _require_thread_reply_approval_action, thread, commit, request
    )


def _require_thread_reply_approval_action(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    if thread.require_reply_approval:
        return False

    thread.require_reply_approval = True

    if commit:
        thread.save()

    return True


def remove_thread_reply_approval(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    return remove_thread_reply_approval_hook(
        _remove_thread_reply_approval_action, thread, commit, request
    )


def _remove_thread_reply_approval_action(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    if not thread.require_reply_approval:
        return False

    thread.require_reply_approval = False

    if commit:
        thread.save()

    return True
