from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Dict, Iterable, Optional

from django.db.models import IntegerChoices
from django.urls import reverse
from django.utils.translation import pgettext, pgettext_lazy

from ..acl.useracl import get_user_acl
from ..categories.enums import CategoryTree
from ..conf.dynamicsettings import DynamicSettings
from ..core.mail import build_mail
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
from ..threads.threadurl import get_thread_url
from .verbs import NotificationVerb
from .models import Notification, WatchedThread
from .users import notify_user

if TYPE_CHECKING:
    from ..users.models import User


class ThreadNotifications(IntegerChoices):
    NONE = 0, pgettext_lazy("notification type", "Don't notify")
    SITE_ONLY = 1, pgettext_lazy("notification type", "Notify on site only")
    SITE_AND_EMAIL = 2, pgettext_lazy(
        "notification type", "Notify on site and with e-mail"
    )


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
    is_private = post.category.tree_id == CategoryTree.PRIVATE_THREADS
    user_acl = get_user_acl(watched_thread.user, cache_versions)

    if not user_can_see_post(watched_thread.user, user_acl, post, is_private):
        return  # Skip this watcher because they can't see the post

    if user_has_other_unread_posts(watched_thread, user_acl, post, is_private):
        return  # We only notify on first unread post

    notify_user(
        watched_thread.user,
        NotificationVerb.REPLIED,
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
    watched_thread: WatchedThread,
    user_acl: dict,
    post: Post,
    is_private: bool,
) -> bool:
    posts_queryset = Post.objects.filter(
        id__lt=post.id,
        thread=post.thread,
        posted_on__gt=watched_thread.read_time,
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
        verb=NotificationVerb.INVITED,
        post=thread.first_post,
        is_read=False,
    ).exists()

    if has_unread_notification:
        return  # Don't spam users with notifications

    notify_user(
        user,
        NotificationVerb.INVITED,
        actor,
        thread.category,
        thread,
        thread.first_post,
    )

    if notification == ThreadNotifications.SITE_AND_EMAIL:
        email_participant_on_new_private_thread(user, actor, watched_thread, settings)


def email_participant_on_new_private_thread(
    user: "User",
    actor: "User",
    watched_thread: WatchedThread,
    settings: DynamicSettings,
):
    thread = watched_thread.thread

    subject = pgettext(
        "new private thread email subject",
        '%(user)s has invited you to participate in private thread "%(thread)s"',
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
                kwargs={"id": thread.id, "slug": thread.slug},
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
    read_time = thread.started_on - timedelta(seconds=5)

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


def user_can_see_private_thread(user: "User", user_acl: dict, thread: Thread) -> bool:
    if not can_use_private_threads(user_acl):
        return False

    is_participant = ThreadParticipant.objects.filter(thread=thread, user=user).exists()
    if not can_see_private_thread(user_acl, thread, is_participant):
        return False

    return True
