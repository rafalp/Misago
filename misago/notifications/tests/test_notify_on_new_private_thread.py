import pytest

from ...privatethreads.models import PrivateThreadMember
from ...users.bans import ban_user
from ..enums import NotificationVerb
from ..models import Notification, WatchedThread
from ..tasks import notify_on_new_private_thread
from ..threads import ThreadNotifications


@pytest.fixture
def notify_user_mock(mocker):
    return mocker.patch("misago.notifications.tasks.notify_user_on_new_private_thread")


def test_notify_on_new_private_thread_does_nothing_if_actor_is_not_found(
    notify_user_mock, other_user, private_thread
):
    notify_on_new_private_thread(other_user.id + 1, private_thread.id, [other_user.id])
    notify_user_mock.assert_not_called()


def test_notify_on_new_private_thread_skips_banned_users(
    notify_user_mock, user, other_user, user_private_thread
):
    other_user.notify_new_private_threads_by_followed = ThreadNotifications.NONE
    other_user.notify_new_private_threads_by_other_users = (
        ThreadNotifications.SITE_AND_EMAIL
    )
    other_user.save()

    PrivateThreadMember.objects.create(user=other_user, thread=user_private_thread)

    ban_user(other_user)

    notify_on_new_private_thread(user.id, user_private_thread.id, [other_user.id])
    notify_user_mock.assert_not_called()


def test_notify_on_new_private_thread_skips_inactive_users(
    notify_user_mock, user, inactive_user, user_private_thread
):
    inactive_user.notify_new_private_threads_by_followed = ThreadNotifications.NONE
    inactive_user.notify_new_private_threads_by_other_users = (
        ThreadNotifications.SITE_AND_EMAIL
    )
    inactive_user.save()

    PrivateThreadMember.objects.create(user=inactive_user, thread=user_private_thread)

    notify_on_new_private_thread(user.id, user_private_thread.id, [inactive_user.id])
    notify_user_mock.assert_not_called()


def test_notify_on_new_private_thread_handles_exceptions(
    mocker, user, other_user, private_thread
):
    PrivateThreadMember.objects.create(user=other_user, thread=private_thread)

    notify_user_mock = mocker.patch(
        "misago.notifications.tasks.notify_user_on_new_private_thread",
        side_effect=ValueError("Unknown"),
    )

    notify_on_new_private_thread(user.id, private_thread.id, [other_user.id])
    notify_user_mock.assert_called_once()


def test_notify_on_new_private_thread_creates_member_watched_thread(
    user, other_user, user_private_thread
):
    other_user.watch_new_private_threads_by_followed = ThreadNotifications.NONE
    other_user.watch_new_private_threads_by_other_users = (
        ThreadNotifications.SITE_AND_EMAIL
    )
    other_user.save()

    PrivateThreadMember.objects.create(user=other_user, thread=user_private_thread)

    notify_on_new_private_thread(user.id, user_private_thread.id, [other_user.id])

    WatchedThread.objects.get(
        user=other_user,
        category=user_private_thread.category,
        thread=user_private_thread,
        send_emails=True,
    )


def test_notify_on_new_private_thread_from_followed_creates_member_watched_thread(
    user, other_user, user_private_thread
):
    other_user.watch_new_private_threads_by_followed = (
        ThreadNotifications.SITE_AND_EMAIL
    )
    other_user.watch_new_private_threads_by_other_users = ThreadNotifications.NONE
    other_user.save()

    other_user.follows.add(user)

    PrivateThreadMember.objects.create(user=other_user, thread=user_private_thread)

    notify_on_new_private_thread(user.id, user_private_thread.id, [other_user.id])

    WatchedThread.objects.get(
        user=other_user,
        category=user_private_thread.category,
        thread=user_private_thread,
        send_emails=True,
    )


def test_notify_on_new_private_thread_notifies_member(
    user, other_user, user_private_thread, mailoutbox
):
    other_user.notify_new_private_threads_by_followed = ThreadNotifications.NONE
    other_user.notify_new_private_threads_by_other_users = ThreadNotifications.SITE_ONLY
    other_user.save()

    PrivateThreadMember.objects.create(user=other_user, thread=user_private_thread)

    notify_on_new_private_thread(user.id, user_private_thread.id, [other_user.id])

    other_user.refresh_from_db()
    assert other_user.unread_notifications == 1

    Notification.objects.get(user=other_user, actor=user)
    assert len(mailoutbox) == 0


def test_notify_on_new_private_thread_notifies_member_with_email(
    user, other_user, user_private_thread, mailoutbox
):
    other_user.notify_new_private_threads_by_followed = ThreadNotifications.NONE
    other_user.notify_new_private_threads_by_other_users = (
        ThreadNotifications.SITE_AND_EMAIL
    )
    other_user.save()

    PrivateThreadMember.objects.create(user=other_user, thread=user_private_thread)

    notify_on_new_private_thread(user.id, user_private_thread.id, [other_user.id])

    other_user.refresh_from_db()
    assert other_user.unread_notifications == 1

    Notification.objects.get(user=other_user, actor=user)
    assert len(mailoutbox) == 1


def test_notify_on_new_private_thread_notifies_member_following_actor(
    user, other_user, user_private_thread, mailoutbox
):
    other_user.notify_new_private_threads_by_followed = ThreadNotifications.SITE_ONLY
    other_user.notify_new_private_threads_by_other_users = ThreadNotifications.NONE
    other_user.save()

    other_user.follows.add(user)

    PrivateThreadMember.objects.create(user=other_user, thread=user_private_thread)

    notify_on_new_private_thread(user.id, user_private_thread.id, [other_user.id])

    other_user.refresh_from_db()
    assert other_user.unread_notifications == 1

    Notification.objects.get(user=other_user, actor=user)
    assert len(mailoutbox) == 0


def test_notify_on_new_private_thread_notifies_member_following_actor_with_email(
    user, other_user, user_private_thread, mailoutbox
):
    other_user.notify_new_private_threads_by_followed = (
        ThreadNotifications.SITE_AND_EMAIL
    )
    other_user.notify_new_private_threads_by_other_users = ThreadNotifications.NONE
    other_user.save()

    other_user.follows.add(user)

    PrivateThreadMember.objects.create(user=other_user, thread=user_private_thread)

    notify_on_new_private_thread(user.id, user_private_thread.id, [other_user.id])

    other_user.refresh_from_db()
    assert other_user.unread_notifications == 1

    Notification.objects.get(user=other_user, actor=user)
    assert len(mailoutbox) == 1


def test_notify_on_new_private_thread_skips_notification_if_one_already_exists(
    user, other_user, user_private_thread, mailoutbox
):
    other_user.notify_new_private_threads_by_followed = ThreadNotifications.NONE
    other_user.notify_new_private_threads_by_other_users = (
        ThreadNotifications.SITE_AND_EMAIL
    )
    other_user.save()

    PrivateThreadMember.objects.create(user=other_user, thread=user_private_thread)

    Notification.objects.create(
        user=other_user,
        verb=NotificationVerb.ADDED_TO_PRIVATE_THREAD,
        category=user_private_thread.category,
        thread=user_private_thread,
        post=user_private_thread.first_post,
        is_read=False,
    )

    notify_on_new_private_thread(user.id, user_private_thread.id, [other_user.id])

    other_user.refresh_from_db()
    assert other_user.unread_notifications == 0

    Notification.objects.count() == 1
    assert len(mailoutbox) == 0


def test_notify_on_new_private_thread_notifies_member_if_old_notification_is_read(
    user, other_user, user_private_thread, mailoutbox
):
    other_user.notify_new_private_threads_by_followed = ThreadNotifications.NONE
    other_user.notify_new_private_threads_by_other_users = (
        ThreadNotifications.SITE_AND_EMAIL
    )
    other_user.save()

    PrivateThreadMember.objects.create(user=other_user, thread=user_private_thread)

    Notification.objects.create(
        user=other_user,
        verb=NotificationVerb.ADDED_TO_PRIVATE_THREAD,
        category=user_private_thread.category,
        thread=user_private_thread,
        post=user_private_thread.first_post,
        is_read=True,
    )

    notify_on_new_private_thread(user.id, user_private_thread.id, [other_user.id])

    other_user.refresh_from_db()
    assert other_user.unread_notifications == 1

    Notification.objects.count() == 2
    assert len(mailoutbox) == 1


def test_notify_on_new_private_thread_skips_member_if_they_have_no_permission(
    user, other_user, members_group, user_private_thread, mailoutbox
):
    other_user.notify_new_private_threads_by_followed = ThreadNotifications.NONE
    other_user.notify_new_private_threads_by_other_users = (
        ThreadNotifications.SITE_AND_EMAIL
    )
    other_user.save()

    PrivateThreadMember.objects.create(user=other_user, thread=user_private_thread)

    members_group.can_use_private_threads = False
    members_group.save()

    notify_on_new_private_thread(user.id, user_private_thread.id, [other_user.id])

    other_user.refresh_from_db()
    assert other_user.unread_notifications == 0

    assert not Notification.objects.exists()
    assert len(mailoutbox) == 0


def test_notify_on_new_private_thread_skips_user_if_not_member(
    user, other_user, user_private_thread, mailoutbox
):
    other_user.notify_new_private_threads_by_followed = ThreadNotifications.NONE
    other_user.notify_new_private_threads_by_other_users = (
        ThreadNotifications.SITE_AND_EMAIL
    )
    other_user.save()

    PrivateThreadMember.objects.filter(user=other_user).delete()

    notify_on_new_private_thread(user.id, user_private_thread.id, [other_user.id])

    other_user.refresh_from_db()
    assert other_user.unread_notifications == 0

    assert not Notification.objects.exists()
    assert len(mailoutbox) == 0
