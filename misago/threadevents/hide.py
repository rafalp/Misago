from django.http import HttpRequest
from django.utils import timezone

from .hooks import hide_thread_update_hook, unhide_thread_update_hook
from .models import ThreadEvent


def hide_thread_event(
    thread_event: ThreadEvent, request: HttpRequest | None = None
) -> bool:
    return hide_thread_update_hook(_hide_thread_event_action, thread_event, request)


def _hide_thread_event_action(
    thread_event: ThreadEvent,
    request: HttpRequest | None = None,
) -> bool:
    if thread_event.is_hidden:
        return False

    thread_event.is_hidden = True
    thread_event.hidden_at = timezone.now()

    if request and request.user.is_authenticated:
        thread_event.hidden_by = request.user
        thread_event.hidden_by_name = request.user.username
        thread_event.hidden_by_slug = request.user.slug

    thread_event.save()
    return True


def unhide_thread_event(
    thread_event: ThreadEvent, request: HttpRequest | None = None
) -> bool:
    return unhide_thread_update_hook(_unhide_thread_event_action, thread_event, request)


def _unhide_thread_event_action(
    thread_event: ThreadEvent,
    request: HttpRequest | None = None,
) -> bool:
    if not thread_event.is_hidden:
        return False

    thread_event.is_hidden = False
    thread_event.hidden_by = None
    thread_event.hidden_by_name = None
    thread_event.hidden_by_slug = None
    thread_event.hidden_at = None
    thread_event.save()

    return True
