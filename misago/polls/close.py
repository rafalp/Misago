from typing import TYPE_CHECKING

from django.http import HttpRequest
from django.utils import timezone

from .hooks import delete_poll_hook
from .models import Poll

if TYPE_CHECKING:
    from ..users.models import User


def close_poll(poll: Poll, user: "User", request: HttpRequest | None = None) -> bool:
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
    if not poll.is_closed:
        return False

    poll.is_closed = False
    poll.closed_at = None
    poll.closed_by = None
    poll.closed_by_name = None
    poll.closed_by_slug = None
    poll.save()

    return True
