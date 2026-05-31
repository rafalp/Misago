from typing import TYPE_CHECKING, Optional, Union

from django.db.models import F

from ..categories.models import Category
from ..threads.models import Post, Thread
from .models import Notification

if TYPE_CHECKING:
    from ..users.models import User


def notify_user(
    user: "User",
    verb: str,
    actor: Optional[Union["User", str]] = None,
    category: Optional[Category] = None,
    thread: Optional[Thread] = None,
    post: Optional[Post] = None,
) -> Notification:
    if isinstance(actor, str):
        actor_obj = None
        actor_name = actor
    elif actor:
        actor_obj = actor
        actor_name = actor.username
    else:
        actor_obj = None
        actor_name = None

    notification = Notification.objects.create(
        user=user,
        verb=verb,
        actor=actor_obj,
        actor_name=actor_name,
        category=category,
        thread=thread,
        thread_title=thread.title if thread else None,
        post=post,
    )

    user.unread_notifications = F("unread_notifications") + 1
    user.save(update_fields=["unread_notifications"])

    return notification
