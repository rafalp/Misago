from django.http import HttpRequest

from .hooks import delete_thread_update_hook
from .models import ThreadEvent


def delete_thread_event(thread_event: ThreadEvent, request: HttpRequest | None = None):
    delete_thread_update_hook(_delete_thread_event_action, thread_event, request)


def _delete_thread_event_action(
    thread_event: ThreadEvent, request: HttpRequest | None = None
):
    thread_event.delete()
    return True
