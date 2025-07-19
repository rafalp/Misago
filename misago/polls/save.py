from typing import TYPE_CHECKING

from django.http import HttpRequest

from ..threads.models import Thread
from ..threadupdates.create import create_started_poll_thread_update
from ..threadupdates.models import ThreadUpdate
from .hooks import edit_thread_poll_hook, save_thread_poll_hook
from .models import Poll, PollVote

if TYPE_CHECKING:
    from ..users.models import User


def edit_thread_poll(
    thread: Thread, poll: Poll, user: "User", request: HttpRequest | None = None
) -> None:
    edit_thread_poll_hook(_edit_thread_poll_action, thread, poll, user, request)


def _edit_thread_poll_action(
    thread: Thread, poll: Poll, user: "User", request: HttpRequest | None = None
) -> None:
    choices_ids = [choice["id"] for choice in poll.choices]
    deleted_votes = (
        PollVote.objects.filter(poll=poll).exclude(choice_id__in=choices_ids).delete()
    )
    if deleted_votes:
        poll.votes = PollVote.objects.filter(poll=poll).count()

    poll.save()


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
