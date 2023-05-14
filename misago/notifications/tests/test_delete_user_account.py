import pytest

from ..models import Notification, WatchedThread


def test_user_delete_deletes_user_notifications(user, other_user):
    notification = Notification.objects.create(
        user=user,
        actor=other_user,
        actor_name=other_user.username,
        verb="TEST",
    )

    user.delete(anonymous_username="Deleted")

    with pytest.raises(Notification.DoesNotExist):
        notification.refresh_from_db()


def test_user_delete_clears_notifications_actor(user, other_user):
    notification = Notification.objects.create(
        user=user,
        actor=other_user,
        actor_name=other_user.username,
        verb="TEST",
    )

    other_user.delete(anonymous_username="Deleted")

    notification.refresh_from_db()
    assert notification.actor is None


def test_user_delete_excludes_other_users_notifications(user, other_user):
    notification = Notification.objects.create(
        user=other_user,
        verb="TEST",
    )

    user.delete(anonymous_username="Deleted")

    notification.refresh_from_db()


def test_user_delete_deletes_users_watched_threads(
    user, thread, watched_thread_factory
):
    watched_thread = watched_thread_factory(user, thread, send_emails=True)

    user.delete(anonymous_username="Deleted")

    with pytest.raises(WatchedThread.DoesNotExist):
        watched_thread.refresh_from_db()


def test_user_delete_excludes_other_users_watched_threads(
    user, other_user, thread, watched_thread_factory
):
    watched_thread = watched_thread_factory(other_user, thread, send_emails=True)

    user.delete(anonymous_username="Deleted")

    watched_thread.refresh_from_db()
