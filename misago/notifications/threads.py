from typing import TYPE_CHECKING, Optional

from django.db.models import IntegerChoices
from django.utils.translation import pgettext_lazy

from ..threads.models import Thread
from .models import WatchedThread

if TYPE_CHECKING:
    from ..users.models import User


class ThreadNotifications(IntegerChoices):
    NONE = 0, pgettext_lazy("notification type", "Don't notify")
    DONT_EMAIL = 1, pgettext_lazy(
        "notification type", "Notify without sending an e-mail"
    )
    SEND_EMAIL = 2, pgettext_lazy("notification type", "Notify with an e-mail")


def get_watched_thread(user: "User", thread: Thread) -> Optional[WatchedThread]:
    return WatchedThread.objects.filter(user=user, thread=thread).order_by("id").first()
