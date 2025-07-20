from django.http import HttpRequest
from django.utils import timezone

from .hooks import hide_thread_update_hook, unhide_thread_update_hook
from .models import ThreadUpdate


def hide_thread_update(
    thread_update: ThreadUpdate, request: HttpRequest | None = None
) -> bool:
    return hide_thread_update_hook(_hide_thread_update_action, thread_update, request)


def _hide_thread_update_action(
    thread_update: ThreadUpdate,
    request: HttpRequest | None = None,
) -> bool:
    if thread_update.is_hidden:
        return False

    thread_update.is_hidden = True
    thread_update.hidden_at = timezone.now()

    if request and request.user.is_authenticated:
        thread_update.hidden_by = request.user
        thread_update.hidden_by_name = request.user.username

    thread_update.save()
    return True


def unhide_thread_update(
    thread_update: ThreadUpdate, request: HttpRequest | None = None
) -> bool:
    return unhide_thread_update_hook(
        _unhide_thread_update_action, thread_update, request
    )


def _unhide_thread_update_action(
    thread_update: ThreadUpdate,
    request: HttpRequest | None = None,
) -> bool:
    if not thread_update.is_hidden:
        return False

    thread_update.is_hidden = False
    thread_update.hidden_by = None
    thread_update.hidden_by_name = None
    thread_update.hidden_at = None
    thread_update.save()

    return True
