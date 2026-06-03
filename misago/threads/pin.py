from django.http import HttpRequest

from .enums import ThreadPinned
from .hooks import (
    pin_thread_hook,
    unpin_thread_hook,
)
from .models import Thread


def pin_thread(
    thread: Thread,
    everywhere: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    return pin_thread_hook(_pin_thread_action, thread, everywhere, commit, request)


def _pin_thread_action(
    thread: Thread,
    everywhere: bool = False,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    if everywhere:
        value = ThreadPinned.EVERYWHERE
    else:
        value = ThreadPinned.CATEGORY

    if thread.pinned == value:
        return False

    thread.pinned = value

    if commit:
        thread.save()

    return True


def unpin_thread(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    return unpin_thread_hook(_unpin_thread_action, thread, commit, request)


def _unpin_thread_action(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    if thread.pinned == ThreadPinned.NONE:
        return False

    thread.pinned = ThreadPinned.NONE

    if commit:
        thread.save()

    return True
