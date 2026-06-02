from django.http import HttpRequest

from .enums import ThreadPinned
from .hooks import (
    pin_thread_globally_hook,
    pin_thread_in_category_hook,
    unpin_thread_hook,
)
from .models import Thread


def pin_thread_globally(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    return pin_thread_globally_hook(
        _pin_thread_globally_action, thread, commit, request
    )


def _pin_thread_globally_action(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    if thread.weight == ThreadPinned.GLOBAL:
        return False

    thread.weight = ThreadPinned.GLOBAL

    if commit:
        thread.save()

    return True


def pin_thread_in_category(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    return pin_thread_in_category_hook(
        _pin_thread_in_category_action, thread, commit, request
    )


def _pin_thread_in_category_action(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    if thread.weight == ThreadPinned.CATEGORY:
        return False

    thread.weight = ThreadPinned.CATEGORY

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
    if thread.weight == ThreadPinned.NONE:
        return False

    thread.weight = ThreadPinned.NONE

    if commit:
        thread.save()

    return True
