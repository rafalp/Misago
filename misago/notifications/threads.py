from typing import TYPE_CHECKING, Dict, Iterable, Optional

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


def get_watched_threads(
    user: "User", threads: Iterable[Thread]
) -> Dict[int, ThreadNotifications]:
    queryset = (
        WatchedThread.objects.filter(user=user, thread__in=threads)
        .order_by("-id")
        .values_list("thread_id", "notifications")
    )

    return {thread_id: notifications for thread_id, notifications in queryset}


def watch_started_thread(user: "User", thread: Thread):
    if user.watch_started_threads:
        WatchedThread.objects.create(
            user=user,
            category=thread.category,
            thread=thread,
            notifications=user.watch_started_threads,
        )


def watch_replied_thread(user: "User", thread: Thread):
    if not user.watch_replied_threads:
        return

    watched_thread = get_watched_thread(user, thread)
    if watched_thread:
        if not watched_thread.notifications:
            watched_thread.notifications = user.watch_replied_threads
            watched_thread.save(update_fields=["notifications"])

    else:
        WatchedThread.objects.create(
            user=user,
            category=thread.category,
            thread=thread,
            notifications=user.watch_replied_threads,
        )
