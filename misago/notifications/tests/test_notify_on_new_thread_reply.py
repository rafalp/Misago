from datetime import timedelta

import pytest
from django.utils import timezone

from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...privatethreadmembers.models import PrivateThreadMember
from ...users.bans import ban_user
from ..models import Notification
from ..tasks import notify_on_new_thread_reply


@pytest.fixture
def notify_watcher_mock(mocker):
    return mocker.patch("misago.notifications.tasks.notify_watcher_on_new_thread_reply")


def test_notify_on_new_thread_reply_does_nothing_for_unwatched_thread(
    notify_watcher_mock, user_reply
):
    notify_on_new_thread_reply(user_reply.id)
    notify_watcher_mock.assert_not_called()


def test_notify_on_new_thread_reply_skips_reply_author(
    watched_thread_factory, notify_watcher_mock, user, thread, user_reply
):
    watched_thread_factory(user, thread, send_emails=True)
    notify_on_new_thread_reply(user_reply.id)
    notify_watcher_mock.assert_not_called()


def test_notify_on_new_thread_reply_skips_watcher_with_deactivated_account(
    watched_thread_factory, notify_watcher_mock, inactive_user, thread, user_reply
):
    watched_thread_factory(inactive_user, thread, send_emails=True)
    notify_on_new_thread_reply(user_reply.id)
    notify_watcher_mock.assert_not_called()


def test_notify_on_new_thread_reply_skips_watcher_with_banned_account(
    watched_thread_factory, notify_watcher_mock, other_user, thread, user_reply
):
    ban_user(other_user)
    watched_thread_factory(other_user, thread, send_emails=True)

    notify_on_new_thread_reply(user_reply.id)
    notify_watcher_mock.assert_not_called()


def test_notify_on_new_thread_reply_handles_exceptions(
    mocker, watched_thread_factory, other_user, thread, user_reply
):
    notify_watcher_mock = mocker.patch(
        "misago.notifications.tasks.notify_watcher_on_new_thread_reply",
        side_effect=ValueError("Unknown"),
    )

    watched_thread_factory(other_user, thread, send_emails=True)

    notify_on_new_thread_reply(user_reply.id)
    notify_watcher_mock.assert_called_once()


def test_notify_on_new_thread_reply_notifies_user_about_thread_reply(
    watched_thread_factory, user, other_user, thread, user_reply, mailoutbox
):
    watched_thread_factory(other_user, thread, send_emails=False)
    notify_on_new_thread_reply(user_reply.id)

    other_user.refresh_from_db()
    assert other_user.unread_notifications == 1

    Notification.objects.get(user=other_user, actor=user)
    assert len(mailoutbox) == 0


def test_notify_on_new_thread_reply_notifies_user_with_email_about_thread_reply(
    watched_thread_factory, user, other_user, thread, user_reply, mailoutbox
):
    watched_thread_factory(other_user, thread, send_emails=True)
    notify_on_new_thread_reply(user_reply.id)

    other_user.refresh_from_db()
    assert other_user.unread_notifications == 1

    Notification.objects.get(user=other_user, actor=user)
    assert len(mailoutbox) == 1


def test_notify_on_new_thread_reply_checks_user_category_permissions(
    watched_thread_factory, other_user, default_category, thread, user_reply, mailoutbox
):
    CategoryGroupPermission.objects.filter(
        category=default_category, permission=CategoryPermission.SEE
    ).delete()

    watched_thread_factory(other_user, thread, send_emails=True)
    notify_on_new_thread_reply(user_reply.id)

    other_user.refresh_from_db()
    assert other_user.unread_notifications == 0

    assert not Notification.objects.exists()
    assert len(mailoutbox) == 0


def test_notify_on_new_thread_reply_checks_user_thread_permissions(
    watched_thread_factory, other_user, thread, user_reply, mailoutbox
):
    thread.is_unapproved = True
    thread.save()

    watched_thread_factory(other_user, thread, send_emails=True)
    notify_on_new_thread_reply(user_reply.id)

    other_user.refresh_from_db()
    assert other_user.unread_notifications == 0

    assert not Notification.objects.exists()
    assert len(mailoutbox) == 0


def test_notify_on_new_thread_reply_checks_user_post_permissions(
    watched_thread_factory, other_user, thread, user_reply, mailoutbox
):
    user_reply.is_unapproved = True
    user_reply.save()

    watched_thread_factory(other_user, thread, send_emails=True)
    notify_on_new_thread_reply(user_reply.id)

    other_user.refresh_from_db()
    assert other_user.unread_notifications == 0

    assert not Notification.objects.exists()
    assert len(mailoutbox) == 0


def test_notify_on_new_thread_reply_checks_user_has_no_older_unread_posts(
    watched_thread_factory, other_user, thread, user_reply, mailoutbox
):
    watched_thread = watched_thread_factory(other_user, thread, send_emails=True)

    # Make thread's first post unread
    watched_thread.read_time = timezone.now() - timedelta(seconds=5)
    watched_thread.save()

    notify_on_new_thread_reply(user_reply.id)

    other_user.refresh_from_db()
    assert other_user.unread_notifications == 0

    assert not Notification.objects.exists()
    assert len(mailoutbox) == 0


def test_notify_on_new_thread_reply_excludes_user_posts_from_unread_check(
    watched_thread_factory, user, other_user, thread, post, user_reply, mailoutbox
):
    watched_thread = watched_thread_factory(other_user, thread, send_emails=True)

    # Make thread's first post unread
    watched_thread.read_time = timezone.now() - timedelta(seconds=5)
    watched_thread.save()

    # Make thread's first post author the watcher
    post.poster = other_user
    post.save()

    notify_on_new_thread_reply(user_reply.id)

    other_user.refresh_from_db()
    assert other_user.unread_notifications == 1

    Notification.objects.get(user=other_user, actor=user)
    assert len(mailoutbox) == 1


def test_notify_on_new_thread_reply_notifies_user_with_email_about_private_thread_reply(
    watched_thread_factory,
    other_user,
    private_thread,
    user,
    private_thread_user_reply,
    mailoutbox,
):
    PrivateThreadMember.objects.create(thread=private_thread, user=other_user)

    watched_thread_factory(other_user, private_thread, send_emails=True)
    notify_on_new_thread_reply(private_thread_user_reply.id)

    other_user.refresh_from_db()
    assert other_user.unread_notifications == 1

    Notification.objects.get(user=other_user, actor=user)
    assert len(mailoutbox) == 1


def test_notify_on_new_thread_reply_checks_if_user_has_private_threads_permission(
    watched_thread_factory,
    other_user,
    private_thread,
    user,
    members_group,
    private_thread_user_reply,
    mailoutbox,
):
    PrivateThreadMember.objects.create(thread=private_thread, user=other_user)

    members_group.can_use_private_threads = False
    members_group.save()

    watched_thread_factory(other_user, private_thread, send_emails=True)
    notify_on_new_thread_reply(private_thread_user_reply.id)

    other_user.refresh_from_db()
    assert other_user.unread_notifications == 0

    assert not Notification.objects.exists()
    assert len(mailoutbox) == 0


def test_notify_on_new_thread_reply_checks_if_user_is_private_thread_participant(
    watched_thread_factory,
    other_user,
    private_thread,
    private_thread_user_reply,
    mailoutbox,
):
    watched_thread_factory(other_user, private_thread, send_emails=True)
    notify_on_new_thread_reply(private_thread_user_reply.id)

    other_user.refresh_from_db()
    assert other_user.unread_notifications == 0

    assert not Notification.objects.exists()
    assert len(mailoutbox) == 0
