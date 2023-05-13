from logging import getLogger

from celery import shared_task
from django.contrib.auth import get_user_model

from ..cache.versions import get_cache_versions
from ..conf.dynamicsettings import DynamicSettings
from ..core.pgutils import chunk_queryset
from ..users.bans import get_user_ban
from ..threads.models import Post, Thread
from .models import WatchedThread
from .threads import (
    notify_participant_on_new_private_thread,
    notify_watcher_on_new_thread_reply,
)

NOTIFY_CHUNK_SIZE = 20

User = get_user_model()
logger = getLogger("misago.notifications")


@shared_task(serializer="json")
def notify_on_new_thread_reply(
    reply_id: int,
):
    post = Post.objects.select_related("poster", "thread", "category").get(id=reply_id)
    post.thread.category = post.category

    if not WatchedThread.objects.filter(thread=post.thread).exists():
        return  # Nobody is watching this thread, stop

    cache_versions = get_cache_versions()
    settings = DynamicSettings(cache_versions)

    queryset = WatchedThread.objects.filter(thread=post.thread).select_related("user")

    for watched_thread in chunk_queryset(queryset, NOTIFY_CHUNK_SIZE):
        if (
            watched_thread.user == post.poster
            or not watched_thread.user.is_active
            or get_user_ban(watched_thread.user, cache_versions)
        ):
            continue  # Skip poster and banned or inactive watchers

        try:
            notify_watcher_on_new_thread_reply(
                watched_thread, post, cache_versions, settings
            )
        except Exception:
            logger.exception("Unexpected error in 'notify_watcher_on_new_thread_reply'")


@shared_task(serializer="json")
def notify_on_new_private_thread(
    actor_id: int,
    thread_id: int,
    participants: list[int],
):
    actor = User.objects.filter(id=actor_id).first()
    thread = (
        Thread.objects.filter(id=thread_id)
        .select_related("category", "first_post")
        .first()
    )

    if not actor or not thread:
        return  # Actor or thread could not be found but we need both

    cache_versions = get_cache_versions()
    settings = DynamicSettings(cache_versions)

    queryset = User.objects.filter(id__in=participants)

    for participant in chunk_queryset(queryset, NOTIFY_CHUNK_SIZE):
        if not participant.is_active or get_user_ban(participant, cache_versions):
            continue  # Skip inactive or banned participants

        try:
            notify_participant_on_new_private_thread(
                participant, actor, thread, cache_versions, settings
            )
        except Exception:
            logger.exception(
                "Unexpected error in 'notify_participant_on_new_private_thread'"
            )
