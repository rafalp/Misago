from typing import TYPE_CHECKING, Optional

from django.http import HttpRequest

from ..threads.models import Thread

if TYPE_CHECKING:
    from ..users.models import User


def get_private_thread_members_context_data(
    request: HttpRequest,
    thread: Thread,
    owner: Optional["User"],
    members: list["User"],
) -> dict:
    moderation = bool(request.user_permissions.is_private_threads_moderator)
    manage = moderation or request.user.id == owner.id if owner else None

    return {
        "manage": manage,
        "moderation": moderation,
        "thread": thread,
        "owner": owner,
        "members": members,
    }
