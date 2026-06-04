from django.http import HttpRequest

from .hooks import approve_thread_hook
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
