from datetime import timedelta
from logging import getLogger
from typing import Dict, Iterable, Optional

from celery import shared_task
from django.contrib.auth import get_user_model
from django.db.models import F
from django.utils.translation import gettext as _

from ..acl.useracl import get_user_acl
from ..cache.versions import get_cache_versions
from ..categories.trees import CategoriesTree
from ..conf.dynamicsettings import DynamicSettings
from ..core.mail import build_mail
from ..core.pgutils import chunk_queryset
from ..threads.models import Post, Thread, ThreadParticipant
from ..threads.permissions.privatethreads import (
    can_see_private_thread,
    can_use_private_threads,
)
from ..threads.permissions.threads import (
    can_see_post,
    can_see_thread,
    exclude_invisible_posts,
)
from .enums import NotificationVerb, ThreadNotifications
from .models import Notification, WatchedThread

User = get_user_model()

logger = getLogger("misago.notifications.threads")

NOTIFY_CHUNK_SIZE = 20


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
def notify_on_new_thread_reply(
    reply_id: int,
):
    # TODO: move `misago.users.bans` to `misago.bans`
    from ..users.bans import get_user_ban

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
            or watched_thread.notifications == ThreadNotifications.NONE
            or not watched_thread.user.is_active
            or get_user_ban(watched_thread.user, cache_versions)
        ):
            continue  # Skip poster and watchers banned or with notifications disabled

        try:
            notify_watcher_on_new_thread_reply(
                watched_thread, post, cache_versions, settings
            )
        except Exception:
            logger.exception("Unexpected error in 'notify_watcher_on_new_thread_reply'")


def notify_watcher_on_new_thread_reply(
    watched_thread: WatchedThread,
    post: Post,
    cache_versions: Dict[str, str],
    settings: DynamicSettings,
):
    is_private = post.category.tree_id == CategoriesTree.PRIVATE_THREADS
    user_acl = get_user_acl(watched_thread.user, cache_versions)

    if not user_can_see_post(watched_thread.user, user_acl, post, is_private):
        return  # Skip this watcher because they can't see the post

    if user_has_other_unread_posts(watched_thread, user_acl, post, is_private):
        return  # We only notify on first unread post

    Notification.objects.create(
        user=watched_thread.user,
        verb=NotificationVerb.REPLIED,
        actor=post.poster,
        actor_name=post.poster.username,
        category=post.category,
        thread=post.thread,
        thread_title=post.thread.title,
        post=post,
    )

    watched_thread.user.unread_notifications = F("unread_notifications") + 1
    watched_thread.user.save(update_fields=["unread_notifications"])

    if watched_thread.notifications == ThreadNotifications.SEND_EMAIL:
        email_watcher_on_new_thread_reply(watched_thread, post, settings)


def email_watcher_on_new_thread_reply(
    watched_thread: WatchedThread,
    post: Post,
    settings: DynamicSettings,
):
    subject = _("%(thread)s - new reply by %(user)s") % {
        "user": post.poster.username,
        "thread": post.thread.title,
    }

    message = build_mail(
        watched_thread.user,
        subject,
        "misago/emails/thread/reply",
        sender=post.poster,
        context={
            "settings": settings,
            "watched_thread": watched_thread,
            "thread": post.thread,
            "post": post,
        },
    )

    message.send()


def user_has_other_unread_posts(
    watched_thread: WatchedThread,
    user_acl: dict,
    post: Post,
    is_private: bool,
) -> bool:
    posts_queryset = Post.objects.filter(
        id__lt=post.id,
        thread=post.thread,
        posted_on__gt=watched_thread.read_at,
    ).exclude(poster=watched_thread.user)

    if not is_private:
        posts_queryset = exclude_invisible_posts(
            user_acl, post.category, posts_queryset
        )

    return posts_queryset.exists()


def user_can_see_post(
    user: "User",
    user_acl: dict,
    post: Post,
    is_private: bool,
) -> bool:
    if is_private:
        return user_can_see_post_in_private_thread(user, user_acl, post)

    return can_see_thread(user_acl, post.thread) and can_see_post(user_acl, post)


def user_can_see_post_in_private_thread(
    user: "User", user_acl: dict, post: Post
) -> bool:
    if not can_use_private_threads(user_acl):
        return False

    is_participant = ThreadParticipant.objects.filter(
        thread=post.thread, user=user
    ).exists()
    if not can_see_private_thread(user_acl, post.thread, is_participant):
        return False

    return True


@shared_task
def notify_on_new_private_thread(
    actor_id: int,
    thread_id: int,
    participants: list[int],
):
    # TODO: move `misago.users.bans` to `misago.bans`
    from ..users.bans import get_user_ban

    actor = User.object.filter(id=actor_id).first()
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
        if get_user_ban(participant, cache_versions):
            continue  # Skip banned participants

        try:
            notify_participant_on_new_private_thread(
                participant, actor, thread, cache_versions, settings
            )
        except Exception:
            logger.exception(
                "Unexpected error in 'notify_participant_on_new_private_thread'"
            )


def notify_participant_on_new_private_thread(
    user: "User",
    actor: "User",
    thread: Thread,
    cache_versions: dict[str, str],
    settings: DynamicSettings,
):
    user_acl = get_user_acl(user, cache_versions)

    if not user_can_see_private_thread(user, user_acl, thread):
        return False  # User can't see private thread

    actor_is_followed = user.follows.has(actor)

    watched_thread = watch_new_private_thread(user, thread, actor_is_followed)

    if actor_is_followed:
        notify = user.notify_new_private_threads_by_followed
    else:
        notify = user.notify_new_private_threads_by_other_users

    if notify == ThreadNotifications.NONE:
        return  # User has disabled notifications for new private threads

    has_unread_notification = Notification.objects.filter(
        user=user,
        verb=NotificationVerb.INVITED,
        post=thread.first_post,
        is_read=False,
    ).exists()

    if has_unread_notification:
        return  # Don't spam users with notifications

    Notification.objects.create(
        user=user,
        verb=NotificationVerb.INVITED,
        actor=actor,
        actor_name=actor.username,
        category=thread.category,
        thread=thread,
        thread_title=thread.title,
        post=thread.first_post,
    )

    user.unread_notifications = F("unread_notifications") + 1
    user.save(update_fields=["unread_notifications"])

    if notify == ThreadNotifications.SEND_EMAIL:
        email_participant_on_new_private_thread(user, actor, watched_thread, settings)


def email_participant_on_new_private_thread(
    user: "User",
    actor: "User",
    watched_thread: WatchedThread,
    settings: DynamicSettings,
):
    thread = watched_thread.thread

    subject = _(
        '%(user)s has invited you to participate in private thread "%(thread)s"'
    )
    subject_formats = {"thread": thread.title, "user": actor.username}

    message = build_mail(
        user,
        subject % subject_formats,
        "misago/emails/privatethread/added",
        sender=actor,
        context={
            "settings": settings,
            "watched_thread": watched_thread,
            "thread": thread,
        },
    )

    message.send()


def watch_new_private_thread(
    user: "User", thread: Thread, from_followed: bool
) -> WatchedThread:
    if from_followed:
        notifications = user.watch_new_private_threads_by_followed
    else:
        notifications = user.watch_new_private_threads_by_other_users

    # Set thread read date in past to prevent first reply to thread
    # From triggering extra notification
    read_at = thread.started_on - timedelta(seconds=5)

    if watched_thread := get_watched_thread(user, thread):
        watched_thread.notifications = notifications
        watched_thread.read_at = read_at
        watched_thread.save(update_fields=["notifications", "read_at"])
        return watched_thread

    return WatchedThread.objects.create(
        user=user,
        category=thread.category,
        thread=thread,
        notifications=notifications,
        read_at=read_at,
    )


def user_can_see_private_thread(user: "User", user_acl: dict, thread: Thread) -> bool:
    if not can_use_private_threads(user_acl):
        return False

    is_participant = ThreadParticipant.objects.filter(thread=thread, user=user).exists()
    if not can_see_private_thread(user_acl, thread, is_participant):
        return False

    return True
