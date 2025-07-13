from typing import TYPE_CHECKING

from django.http import HttpRequest

from ..threads.models import Thread
from ..threadupdates.create import create_started_poll_thread_update
from ..threadupdates.models import ThreadUpdate
from .hooks import save_thread_poll_hook
from .models import Poll

if TYPE_CHECKING:
    from ..users.models import User


def save_thread_poll(
    thread: Thread, poll: Poll, user: "User", request: HttpRequest | None = None
) -> ThreadUpdate:
    return save_thread_poll_hook(_save_thread_poll_action, thread, poll, user, request)


def _save_thread_poll_action(
    thread: Thread, poll: Poll, user: "User", request: HttpRequest | None = None
) -> ThreadUpdate:
    poll.save()

    thread.has_poll = True
    thread.save()

    return create_started_poll_thread_update(thread, poll, user, request)
