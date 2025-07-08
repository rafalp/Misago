from typing import TYPE_CHECKING

from django.http import HttpRequest
from django.utils import timezone

from ..threads.models import Thread
from ..threadupdates.models import ThreadUpdate
from ..threadupdates.create import (
    create_closed_poll_thread_update,
    create_opened_poll_thread_update,
)
from .hooks import (
    close_poll_hook,
    close_thread_poll_hook,
    open_poll_hook,
    open_thread_poll_hook,
)
from .models import Poll

if TYPE_CHECKING:
    from ..users.models import User


def close_thread_poll(
    thread: Thread, poll: Poll, user: "User", request: HttpRequest | None = None
) -> ThreadUpdate | None:
    return close_thread_poll_hook(
        _close_thread_poll_action, thread, poll, user, request
    )


def _close_thread_poll_action(
    thread: Thread, poll: Poll, user: "User", request: HttpRequest | None = None
) -> ThreadUpdate | None:
    if not close_poll(poll, user, request):
        return None

    return create_closed_poll_thread_update(thread, user, request)


def open_thread_poll(
    thread: Thread, poll: Poll, user: "User", request: HttpRequest | None = None
) -> ThreadUpdate | None:
    return open_thread_poll_hook(_open_thread_poll_action, thread, poll, user, request)


def _open_thread_poll_action(
    thread: Thread, poll: Poll, user: "User", request: HttpRequest | None = None
) -> ThreadUpdate | None:
    if not open_poll(poll, user, request):
        return None

    return create_opened_poll_thread_update(thread, user, request)


def close_poll(poll: Poll, user: "User", request: HttpRequest | None = None) -> bool:
    return close_poll_hook(_close_poll_action, poll, user, request)


def _close_poll_action(
    poll: Poll, user: "User", request: HttpRequest | None = None
) -> bool:
    if poll.is_closed:
        return False

    poll.is_closed = True
    poll.closed_at = timezone.now()
    poll.closed_by = user
    poll.closed_by_name = user.username
    poll.closed_by_slug = user.slug
    poll.save()

    return True


def open_poll(poll: Poll, user: "User", request: HttpRequest | None = None) -> bool:
    return open_poll_hook(_open_poll_action, poll, user, request)


def _open_poll_action(
    poll: Poll, user: "User", request: HttpRequest | None = None
) -> bool:
    if not poll.is_closed:
        return False

    poll.is_closed = False
    poll.closed_at = None
    poll.closed_by = None
    poll.closed_by_name = None
    poll.closed_by_slug = None
    poll.save()

    return True
