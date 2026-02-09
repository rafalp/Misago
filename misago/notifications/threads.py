from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Dict, Iterable, Optional

from django.http import HttpRequest
from django.urls import reverse
from django.utils.translation import pgettext

from ..conf.dynamicsettings import DynamicSettings
from ..core.mail import build_mail
from ..permissions.checkutils import check_permissions
from ..permissions.generic import (
    check_access_post_permission,
    filter_accessible_thread_posts,
)
from ..permissions.proxy import UserPermissionsProxy
from ..permissions.privatethreads import (
    check_private_threads_permission,
    check_see_private_thread_permission,
)
from ..threads.models import Post, Thread
from ..threads.threadurl import get_thread_url
from .enums import NotificationVerb, ThreadNotifications
from .hooks import unwatch_thread_hook, watch_thread_hook
from .models import Notification, WatchedThread
from .users import notify_user

if TYPE_CHECKING:
    from ..users.models import User


def watch_thread(
    thread: Thread,
    user: "User",
    send_emails: bool = True,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> WatchedThread:
    return watch_thread_hook(
        _watch_thread_action, thread, user, send_emails, commit, request
    )


def _watch_thread_action(
    thread: Thread,
    user: "User",
    send_emails: bool = True,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> WatchedThread:
    watched_thread = WatchedThread(
        user=user,
        category=thread.category,
        thread=thread,
        send_emails=send_emails,
    )

    if commit:
        watched_thread.save()

    return watched_thread


def unwatch_thread(
    thread: Thread,
    user: "User",
    request: HttpRequest | None = None,
) -> bool:
    return unwatch_thread_hook(_unwatch_thread_action, thread, user, request)


def _unwatch_thread_action(
    thread: Thread,
    user: "User",
    request: HttpRequest | None = None,
) -> bool:
    deleted_rows, _ = WatchedThread.objects.filter(user=user, thread=thread).delete()
    return bool(deleted_rows)


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
        .values_list("thread_id", "send_emails")
    )

    return {
        thread_id: (
            ThreadNotifications.SITE_AND_EMAIL
            if send_emails
            else ThreadNotifications.SITE_ONLY
        )
        for thread_id, send_emails in queryset
    }


def watch_started_thread(user: "User", thread: Thread):
    if user.watch_started_threads:
        WatchedThread.objects.create(
            user=user,
            category=thread.category,
            thread=thread,
            send_emails=user.watch_started_threads
            == ThreadNotifications.SITE_AND_EMAIL,
        )


def watch_replied_thread(user: "User", thread: Thread) -> WatchedThread | None:
    if not user.watch_replied_threads:
        return

    if WatchedThread.objects.filter(user=user, thread=thread).exists():
        return None

    send_emails = user.watch_replied_threads == ThreadNotifications.SITE_AND_EMAIL

    return WatchedThread.objects.create(
        user=user,
        category=thread.category,
        thread=thread,
        send_emails=send_emails,
    )


def update_watched_thread_read_time(user: "User", thread: Thread, read_time: datetime):
    WatchedThread.objects.filter(user=user, thread=thread).update(read_time=read_time)


def notify_watcher_on_new_thread_reply(
    watched_thread: WatchedThread,
    post: Post,
    cache_versions: Dict[str, str],
    settings: DynamicSettings,
):
    user_permissions = UserPermissionsProxy(watched_thread.user, cache_versions)

    with check_permissions() as can_see_post:
        check_access_post_permission(user_permissions, post.category, post.thread, post)

    if not can_see_post:
        return  # Skip this watcher because they can't see the post

    if user_has_other_unread_posts(user_permissions, watched_thread, post):
        return  # We only notify on first unread post

    notify_user(
        watched_thread.user,
        NotificationVerb.REPLIED_TO_THREAD,
        post.poster,
        post.category,
        post.thread,
        post,
    )

    if watched_thread.send_emails:
        email_watcher_on_new_thread_reply(watched_thread, post, settings)


def email_watcher_on_new_thread_reply(
    watched_thread: WatchedThread,
    post: Post,
    settings: DynamicSettings,
):
    subject = pgettext(
        "new thread reply email subject", "%(thread)s - new reply by %(user)s"
    ) % {
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
            "thread_url": get_thread_url(post.thread),
            "post": post,
        },
    )

    message.send()


def user_has_other_unread_posts(
    user_permissions: UserPermissionsProxy,
    watched_thread: WatchedThread,
    post: Post,
) -> bool:
    posts_queryset = Post.objects.filter(
        id__lt=post.id,
        thread=post.thread,
        posted_at__gt=watched_thread.read_time,
    ).exclude(poster=watched_thread.user)

    posts_queryset = filter_accessible_thread_posts(
        user_permissions, post.category, post.thread, posts_queryset
    )

    return posts_queryset.exists()


def notify_user_on_new_private_thread(
    user: "User",
    actor: "User",
    thread: Thread,
    cache_versions: dict[str, str],
    settings: DynamicSettings,
):
    user_permissions = UserPermissionsProxy(user, cache_versions)

    with check_permissions() as can_see_private_thread:
        check_private_threads_permission(user_permissions)
        check_see_private_thread_permission(user_permissions, thread)

    if not can_see_private_thread:
        return False  # User can't see private thread

    actor_is_followed = user.is_following(actor)

    watched_thread = watch_new_private_thread(user, thread, actor_is_followed)

    if actor_is_followed:
        notification = user.notify_new_private_threads_by_followed
    else:
        notification = user.notify_new_private_threads_by_other_users

    if notification == ThreadNotifications.NONE:
        return  # User has disabled notifications for new private threads

    has_unread_notification = Notification.objects.filter(
        user=user,
        verb=NotificationVerb.ADDED_TO_PRIVATE_THREAD,
        post=thread.first_post,
        is_read=False,
    ).exists()

    if has_unread_notification:
        return  # Don't spam users with notifications

    notify_user(
        user,
        NotificationVerb.ADDED_TO_PRIVATE_THREAD,
        actor,
        thread.category,
        thread,
        thread.first_post,
    )

    if notification == ThreadNotifications.SITE_AND_EMAIL:
        email_user_on_new_private_thread(user, actor, watched_thread, settings)


def email_user_on_new_private_thread(
    user: "User",
    actor: "User",
    watched_thread: WatchedThread,
    settings: DynamicSettings,
):
    thread = watched_thread.thread

    subject = pgettext(
        "new private thread email subject",
        '%(user)s added you to the private thread "%(thread)s"',
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
            "thread_url": reverse(
                "misago:private-thread",
                kwargs={"thread_id": thread.id, "slug": thread.slug},
            ),
        },
    )

    message.send()


def watch_new_private_thread(
    user: "User", thread: Thread, from_followed: bool
) -> WatchedThread | None:
    if from_followed:
        notifications = user.watch_new_private_threads_by_followed
    else:
        notifications = user.watch_new_private_threads_by_other_users

    if not notifications:
        return None

    send_emails = notifications == ThreadNotifications.SITE_AND_EMAIL

    # Set thread read date in past to prevent first reply to thread
    # From triggering extra notification
    read_time = thread.started_at - timedelta(seconds=5)

    if watched_thread := get_watched_thread(user, thread):
        watched_thread.read_time = read_time
        watched_thread.save(update_fields=["read_time"])
        return watched_thread

    return WatchedThread.objects.create(
        user=user,
        category=thread.category,
        thread=thread,
        send_emails=send_emails,
        read_time=read_time,
    )
