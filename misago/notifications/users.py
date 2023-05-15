from typing import TYPE_CHECKING, Optional

from django.db.models import F

from ..categories.models import Category
from ..threads.models import Post, Thread
from .models import Notification

if TYPE_CHECKING:
    from ..users.models import User


def notify_user(
    user: "User",
    verb: str,
    actor: Optional["User"] = None,
    category: Optional[Category] = None,
    thread: Optional[Thread] = None,
    post: Optional[Post] = None,
) -> Notification:
    notification = Notification.objects.create(
        user=user,
        verb=verb,
        actor=actor,
        actor_name=actor.username if actor else None,
        category=category,
        thread=thread,
        thread_title=thread.title if thread else None,
        post=post,
    )

    user.unread_notifications = F("unread_notifications") + 1
    user.save(update_fields=["unread_notifications"])

    return notification
