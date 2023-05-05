from logging import getLogger
from typing import TYPE_CHECKING, Dict, Iterable, Optional

from celery import shared_task
from django.db.models import F, IntegerChoices
from django.utils.translation import pgettext_lazy

from ..core.pgutils import chunk_queryset
from ..threads.models import Post, Thread
from .verbs import NotificationVerb
from .models import Notification, WatchedThread

if TYPE_CHECKING:
    from ..users.models import User


logger = getLogger("misago.notifications.threads")

NOTIFY_CHUNK_SIZE = 20


class ThreadNotifications(IntegerChoices):
    NONE = 0, pgettext_lazy("notification type", "Don't notify")
    DONT_EMAIL = 1, pgettext_lazy(
        "notification type", "Notify without sending an e-mail"
    )
    SEND_EMAIL = 2, pgettext_lazy("notification type", "Notify with an e-mail")


def get_watched_thread(user: "User", thread: Thread) -> Optional[WatchedThread]:
    """Returns watched thread entry for given user and thread combo.

    If multiple entries are returned, it quietly heals this user's watching entry.
    """
    watched_threads = WatchedThread.objects.filter(user=user, thread=thread).order_by(
        "id"
    )[:2]
    if not watched_threads:
        return None

    watched_thread = watched_threads[0]
    if len(watched_threads) > 1:
        WatchedThread.objects.filter(user=user, thread=thread).exclude(
            id=watched_thread.id
        ).delete()

    return watched_thread


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


@shared_task
def notify_about_new_thread_reply(
    reply_id: int,
    is_private: bool,
):
    post = Post.objects.select_related().get(id=reply_id)
    category = post.category
    thread = post.thread
    poster = post.poster

    thread.category = category

    if not WatchedThread.objects.filter(thread=thread).exists():
        return  # Nobody is watching this thread, stop

    queryset = (
        WatchedThread.objects.filter(thread=thread)
        .exclude(user=poster)
        .select_related("user")
    )

    for watched_thread in chunk_queryset(queryset, NOTIFY_CHUNK_SIZE):
        if watched_thread.notifications == ThreadNotifications.NONE:
            continue  # Skip this watcher because they don't want notifications

        Notification.objects.create(
            user=watched_thread.user,
            verb=NotificationVerb.REPLIED,
            actor=poster,
            actor_name=poster.username,
            category=category,
            thread=thread,
            thread_title=thread.title,
            post=post,
        )

        watched_thread.user.unread_notifications = F("unread_notifications") + 1
        watched_thread.user.save(update_fields=["unread_notifications"])
