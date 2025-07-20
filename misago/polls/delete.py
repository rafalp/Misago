from typing import TYPE_CHECKING

from django.http import HttpRequest

from ..postgres.delete import delete_all, delete_one
from ..threads.models import Thread
from ..threadupdates.create import create_deleted_poll_thread_update
from ..threadupdates.models import ThreadUpdate
from .hooks import delete_poll_hook, delete_thread_poll_hook
from .models import Poll, PollVote

if TYPE_CHECKING:
    from ..users.models import User


def delete_thread_poll(
    thread: Thread, poll: Poll, user: "User", request: HttpRequest | None = None
) -> ThreadUpdate:
    return delete_thread_poll_hook(
        _delete_thread_poll_action, thread, poll, user, request
    )


def _delete_thread_poll_action(
    thread: Thread, poll: Poll, user: "User", request: HttpRequest | None = None
) -> ThreadUpdate:
    delete_poll(poll, request)

    thread.has_poll = False
    thread.save(update_fields=["has_poll"])

    return create_deleted_poll_thread_update(thread, poll, user, request)


def delete_poll(poll: Poll, request: HttpRequest | None = None):
    delete_poll_hook(_delete_poll_action, poll, request)


def _delete_poll_action(poll: Poll, request: HttpRequest | None):
    delete_all(PollVote, poll_id=poll.id)
    delete_one(poll)
