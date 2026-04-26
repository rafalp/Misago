from django.http import HttpRequest

from .hooks import hide_thread_hook, unhide_thread_hook
from .models import Thread


def hide_thread(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    return hide_thread_hook(_hide_thread_action, thread, commit, request)


def _hide_thread_action(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    if thread.is_hidden:
        return False

    thread.is_hidden = True

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

    if commit:
        thread.save()

    return True
