from logging import getLogger
from typing import TYPE_CHECKING, Dict, Iterable, Optional

from celery import shared_task
from django.db.models import F, IntegerChoices
from django.utils.translation import gettext as _, pgettext_lazy

from ..acl.useracl import get_user_acl
from ..cache.versions import get_cache_versions
from ..categories.trees import CategoriesTrees
from ..conf.dynamicsettings import DynamicSettings
from ..core.mail import build_mail, send_messages
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
            or watched_thread.notifications == ThreadNotifications.NONE
        ):
            continue  # Skip poster and watchers with notifications disabled

        try:
            notify_watcher_about_new_thread_reply(
                watched_thread, post, cache_versions, settings
            )
        except Exception:
            logger.exception(
                "Unexpected error in 'notify_watcher_about_new_thread_reply'"
            )


def notify_watcher_about_new_thread_reply(
    watched_thread: WatchedThread,
    post: Post,
    cache_versions: Dict[str, str],
    settings: DynamicSettings,
):
    is_private = post.category.tree_id == CategoriesTrees.PRIVATE_THREADS
    watcher_acl = get_user_acl(watched_thread.user, cache_versions)

    if not watcher_can_see_post(watched_thread.user, watcher_acl, post, is_private):
        return  # Skip this watcher because they can't see the post

    if watcher_has_other_unread_posts(watched_thread, watcher_acl, post, is_private):
        return  # We only notify about first unread post

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
        email_watcher_about_new_thread_reply(watched_thread, post, is_private, settings)


def email_watcher_about_new_thread_reply(
    watched_thread: WatchedThread,
    post: Post,
    is_private: bool,
    settings: DynamicSettings,
):
    message = build_mail(
        watched_thread.user,
        get_new_reply_email_subject(watched_thread, post, is_private),
        "misago/emails/thread/reply",
        sender=post.poster,
        context={
            "settings": settings,
            "watched_thread": watched_thread,
            "thread": post.thread,
            "post": post,
        },
    )

    send_messages([message])


def get_new_reply_email_subject(
    watched_thread: WatchedThread,
    post: Post,
    is_private: bool,
) -> str:
    formats = {"user": post.poster.username, "thread": post.thread.title}

    if is_private:
        if watched_thread.user_id == post.thread.starter_id:
            return (
                _('%(user)s has replied to your private thread "%(thread)s"') % formats
            )

        return (
            _(
                '%(user)s has replied to private thread "%(thread)s" that you are watching'
            )
            % formats
        )

    if watched_thread.user.id == post.thread.starter_id:
        return _('%(user)s has replied to your thread "%(thread)s"') % formats

    return (
        _('%(user)s has replied to a thread "%(thread)s" that you are watching')
        % formats
    )


def watcher_can_see_post(
    watcher: "User",
    watcher_acl: dict,
    post: "Post",
    is_private: bool,
) -> bool:
    if is_private:
        return watcher_can_see_post_in_private_thread(watcher, watcher_acl, post)

    return can_see_thread(watcher_acl, post.thread) and can_see_post(watcher_acl, post)


def watcher_can_see_post_in_private_thread(
    watcher: "User", watcher_acl: dict, post: "Post"
) -> bool:
    if not can_use_private_threads(watcher_acl):
        return False

    is_participant = ThreadParticipant.objects.filter(
        thread=post.thread, user=watcher
    ).exists()
    if not can_see_private_thread(watcher_acl, post.thread, is_participant):
        return False

    return True


def watcher_has_other_unread_posts(
    watched_thread: WatchedThread,
    watcher_acl: dict,
    post: Post,
    is_private: bool,
) -> bool:
    posts_queryset = Post.objects.filter(
        id__lt=post.id,
        thread=post.thread,
        posted_on__gt=watched_thread.read_at,
    ).exclude(poster=post.poster)

    if not is_private:
        posts_queryset = exclude_invisible_posts(
            watcher_acl, post.category, posts_queryset
        )

    return posts_queryset.exists()
