from logging import getLogger

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Count

from ..cache.versions import get_cache_versions
from ..conf.dynamicsettings import DynamicSettings
from ..threads.models import Post, Thread
from ..users.bans import get_user_ban
from .models import WatchedThread
from .threads import (
    notify_user_on_new_private_thread,
    notify_watcher_on_new_thread_reply,
)

NOTIFY_CHUNK_SIZE = 32

User = get_user_model()
logger = getLogger("misago.notifications")


@shared_task(
    name="notifications.new-thread-reply",
    autoretry_for=(Post.DoesNotExist,),
    default_retry_delay=settings.MISAGO_NOTIFICATIONS_RETRY_DELAY,
    serializer="json",
)
def notify_on_new_thread_reply(reply_id: int):
    post = Post.objects.select_related("poster", "thread", "category").get(id=reply_id)
    post.thread.category = post.category

    if not WatchedThread.objects.filter(thread=post.thread).exists():
        return  # Nobody is watching this thread, stop

    cache_versions = get_cache_versions()
    dynamic_settings = DynamicSettings(cache_versions)

    queryset = WatchedThread.objects.filter(thread=post.thread).select_related("user")

    for watched_thread in queryset.iterator(chunk_size=NOTIFY_CHUNK_SIZE):
        if (
            watched_thread.user == post.poster
            or not watched_thread.user.is_active
            or get_user_ban(watched_thread.user, cache_versions)
        ):
            continue  # Skip poster and banned or inactive watchers

        try:
            notify_watcher_on_new_thread_reply(
                watched_thread, post, cache_versions, dynamic_settings
            )
        except Exception:
            logger.exception("Unexpected error in 'notify_watcher_on_new_thread_reply'")


@shared_task(
    name="notifications.new-private-thread",
    autoretry_for=(Thread.DoesNotExist,),
    default_retry_delay=settings.MISAGO_NOTIFICATIONS_RETRY_DELAY,
    serializer="json",
)
def notify_on_new_private_thread(
    actor_id: int,
    thread_id: int,
    members: list[int],
):
    actor = User.objects.filter(id=actor_id).first()
    if not actor:
        return

    thread = Thread.objects.select_related("category", "first_post").get(id=thread_id)

    cache_versions = get_cache_versions()
    dynamic_settings = DynamicSettings(cache_versions)

    queryset = User.objects.filter(id__in=members)

    for user in queryset.iterator(chunk_size=NOTIFY_CHUNK_SIZE):
        if not user.is_active or get_user_ban(user, cache_versions):
            continue  # Skip inactive or banned membmers

        try:
            notify_user_on_new_private_thread(
                user, actor, thread, cache_versions, dynamic_settings
            )
        except Exception:
            logger.exception("Unexpected error in 'notify_user_on_new_private_thread'")


@shared_task(serializer="json")
def delete_duplicate_watched_threads(thread_id: int):
    queryset = (
        WatchedThread.objects.filter(
            thread_id=thread_id,
            user_id__in=(
                WatchedThread.objects.filter(
                    thread_id=thread_id,
                )
                .values("user_id")
                .annotate(entries=Count("user_id"))
                .filter(entries__gt=1)
                .values("user_id")
            ),
        )
        .order_by("user_id", "-read_time", "-id")
        .distinct("user_id")
    )

    for watched_thread in queryset.iterator():
        if not watched_thread.send_emails:
            watched_thread.send_emails = WatchedThread.objects.filter(
                thread_id=thread_id, user_id=watched_thread.user_id, send_emails=True
            ).exists()

            if watched_thread.send_emails:
                watched_thread.save()

        WatchedThread.objects.filter(
            thread_id=thread_id,
            user_id=watched_thread.user_id,
        ).exclude(id=watched_thread.id).delete()
