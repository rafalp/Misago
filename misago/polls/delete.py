from django.http import HttpRequest

from ..postgres.delete import delete_all, delete_one
from .hooks import delete_poll_hook
from .models import Poll, PollVote


def delete_poll(poll: Poll, request: HttpRequest | None = None):
    delete_poll_hook(_delete_poll_action, poll, request)


def _delete_poll_action(poll: Poll, request: HttpRequest | None):
    delete_all(PollVote, poll_id=poll.id)
    delete_one(poll)
