import pytest

from ...threads.models import ThreadParticipant
from ..enums import ThreadNotifications
from ..models import WatchedThread
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
