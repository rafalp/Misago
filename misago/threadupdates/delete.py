from django.http import HttpRequest

from .hooks import delete_thread_update_hook
from .models import ThreadUpdate


def delete_thread_update(
    thread_update: ThreadUpdate, request: HttpRequest | None = None
):
    delete_thread_update_hook(_delete_thread_update_action, thread_update, request)


def _delete_thread_update_action(
    thread_update: ThreadUpdate, request: HttpRequest | None = None
):
    thread_update.delete()
    return True
