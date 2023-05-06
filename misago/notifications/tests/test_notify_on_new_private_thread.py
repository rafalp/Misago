import pytest

from ...threads.models import ThreadParticipant
from ..enums import NotificationVerb, ThreadNotifications
from ..models import Notification, WatchedThread
from ..threads import notify_on_new_private_thread


@pytest.fixture
def notify_participant_mock(mocker):
    return mocker.patch(
        "misago.notifications.threads.notify_participant_on_new_private_thread"
    )


def test_notify_on_new_private_thread_does_nothing_if_actor_is_not_found(
    notify_participant_mock, other_user, private_thread
):
    notify_on_new_private_thread(other_user.id + 1, private_thread.id, [other_user.id])
    notify_participant_mock.assert_not_called()


def test_notify_on_new_private_thread_does_nothing_if_thread_is_not_found(
    notify_participant_mock, user, other_user, private_thread
):
    notify_on_new_private_thread(user.id, private_thread.id + 1, [other_user.id])
    notify_participant_mock.assert_not_called()


def test_notify_on_new_private_thread_handles_exceptions(
    mocker, user, other_user, private_thread
):
    ThreadParticipant.objects.create(user=other_user, thread=private_thread)

    notify_participant_mock = mocker.patch(
        "misago.notifications.threads.notify_participant_on_new_private_thread",
        side_effect=ValueError("Unknown"),
    )

    notify_on_new_private_thread(user.id, private_thread.id, [other_user.id])
    notify_participant_mock.assert_called_once()


def test_notify_on_new_private_thread_creates_participant_watched_thread(
    user, other_user, user_private_thread
):
    other_user.watch_new_private_threads_by_followed = ThreadNotifications.NONE
    other_user.watch_new_private_threads_by_other_users = ThreadNotifications.SEND_EMAIL
    other_user.save()

    ThreadParticipant.objects.create(user=other_user, thread=user_private_thread)

    notify_on_new_private_thread(user.id, user_private_thread.id, [other_user.id])

    WatchedThread.objects.get(
        user=other_user,
        category=user_private_thread.category,
        thread=user_private_thread,
        notifications=ThreadNotifications.SEND_EMAIL,
    )


def test_notify_on_new_private_thread_from_followed_creates_participant_watched_thread(
    user, other_user, user_private_thread
):
    other_user.watch_new_private_threads_by_followed = ThreadNotifications.SEND_EMAIL
    other_user.watch_new_private_threads_by_other_users = ThreadNotifications.NONE
    other_user.save()

    other_user.follows.add(user)

    ThreadParticipant.objects.create(user=other_user, thread=user_private_thread)

    notify_on_new_private_thread(user.id, user_private_thread.id, [other_user.id])

    WatchedThread.objects.get(
        user=other_user,
        category=user_private_thread.category,
        thread=user_private_thread,
        notifications=ThreadNotifications.SEND_EMAIL,
    )


def test_notify_on_new_private_thread_notifies_participant(
    user, other_user, user_private_thread, mailoutbox
):
    other_user.notify_new_private_threads_by_followed = ThreadNotifications.NONE
    other_user.notify_new_private_threads_by_other_users = (
        ThreadNotifications.DONT_EMAIL
    )
    other_user.save()

    ThreadParticipant.objects.create(user=other_user, thread=user_private_thread)

    notify_on_new_private_thread(user.id, user_private_thread.id, [other_user.id])

    other_user.refresh_from_db()
    assert other_user.unread_notifications == 1

    Notification.objects.get(user=other_user, actor=user)
    assert len(mailoutbox) == 0


def test_notify_on_new_private_thread_notifies_participant_with_email(
    user, other_user, user_private_thread, mailoutbox
):
    other_user.notify_new_private_threads_by_followed = ThreadNotifications.NONE
    other_user.notify_new_private_threads_by_other_users = (
        ThreadNotifications.SEND_EMAIL
    )
    other_user.save()

    ThreadParticipant.objects.create(user=other_user, thread=user_private_thread)

    notify_on_new_private_thread(user.id, user_private_thread.id, [other_user.id])

    other_user.refresh_from_db()
    assert other_user.unread_notifications == 1

    Notification.objects.get(user=other_user, actor=user)
    assert len(mailoutbox) == 1


def test_notify_on_new_private_thread_notifies_participant_following_actor(
    user, other_user, user_private_thread, mailoutbox
):
    other_user.notify_new_private_threads_by_followed = ThreadNotifications.DONT_EMAIL
    other_user.notify_new_private_threads_by_other_users = ThreadNotifications.NONE
    other_user.save()

    other_user.follows.add(user)

    ThreadParticipant.objects.create(user=other_user, thread=user_private_thread)

    notify_on_new_private_thread(user.id, user_private_thread.id, [other_user.id])

    other_user.refresh_from_db()
    assert other_user.unread_notifications == 1

    Notification.objects.get(user=other_user, actor=user)
    assert len(mailoutbox) == 0


def test_notify_on_new_private_thread_notifies_participant_following_actor_with_email(
    user, other_user, user_private_thread, mailoutbox
):
    other_user.notify_new_private_threads_by_followed = ThreadNotifications.SEND_EMAIL
    other_user.notify_new_private_threads_by_other_users = ThreadNotifications.NONE
    other_user.save()

    other_user.follows.add(user)

    ThreadParticipant.objects.create(user=other_user, thread=user_private_thread)

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
        ThreadNotifications.SEND_EMAIL
    )
    other_user.save()

    ThreadParticipant.objects.create(user=other_user, thread=user_private_thread)

    Notification.objects.create(
        user=other_user,
        verb=NotificationVerb.INVITED,
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


def test_notify_on_new_private_thread_notifies_participant_if_old_notification_is_read(
    user, other_user, user_private_thread, mailoutbox
):
    other_user.notify_new_private_threads_by_followed = ThreadNotifications.NONE
    other_user.notify_new_private_threads_by_other_users = (
        ThreadNotifications.SEND_EMAIL
    )
    other_user.save()

    ThreadParticipant.objects.create(user=other_user, thread=user_private_thread)

    Notification.objects.create(
        user=other_user,
        verb=NotificationVerb.INVITED,
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


def test_notify_on_new_private_thread_skips_participant_if_they_have_no_permission(
    mocker, user, other_user, user_private_thread, mailoutbox
):
    other_user.notify_new_private_threads_by_followed = ThreadNotifications.NONE
    other_user.notify_new_private_threads_by_other_users = (
        ThreadNotifications.SEND_EMAIL
    )
    other_user.save()

    ThreadParticipant.objects.create(user=other_user, thread=user_private_thread)

    can_use_private_threads_mock = mocker.patch(
        "misago.notifications.threads.can_use_private_threads",
        return_value=False,
    )

    notify_on_new_private_thread(user.id, user_private_thread.id, [other_user.id])

    other_user.refresh_from_db()
    assert other_user.unread_notifications == 0

    assert not Notification.objects.exists()
    assert len(mailoutbox) == 0

    can_use_private_threads_mock.assert_called_once()


def test_notify_on_new_private_thread_skips_user_not_participating(
    mocker, user, other_user, user_private_thread, mailoutbox
):
    other_user.notify_new_private_threads_by_followed = ThreadNotifications.NONE
    other_user.notify_new_private_threads_by_other_users = (
        ThreadNotifications.SEND_EMAIL
    )
    other_user.save()

    notify_on_new_private_thread(user.id, user_private_thread.id, [other_user.id])

    other_user.refresh_from_db()
    assert other_user.unread_notifications == 0

    assert not Notification.objects.exists()
    assert len(mailoutbox) == 0
