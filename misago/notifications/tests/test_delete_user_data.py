import pytest

from ..models import Notification, WatchedThread


def test_user_content_delete_deletes_user_notifications(user, other_user):
    notification = Notification.objects.create(
        user=user,
        actor=other_user,
        actor_name=other_user.username,
        verb="TEST",
    )

    user.delete_content()

    with pytest.raises(Notification.DoesNotExist):
        notification.refresh_from_db()


def test_user_content_delete_deletes_actor_notifications(user, other_user):
    notification = Notification.objects.create(
        user=user,
        actor=other_user,
        actor_name=other_user.username,
        verb="TEST",
    )

    other_user.delete_content()

    with pytest.raises(Notification.DoesNotExist):
        notification.refresh_from_db()


def test_user_content_delete_excludes_other_users_notifications(user, other_user):
    notification = Notification.objects.create(
        user=other_user,
        verb="TEST",
    )

    user.delete_content()

    notification.refresh_from_db()


def test_user_content_delete_deletes_users_watched_threads(
    user, thread, watched_thread_factory
):
    watched_thread = watched_thread_factory(user, thread, send_emails=True)

    user.delete_content()

    with pytest.raises(WatchedThread.DoesNotExist):
        watched_thread.refresh_from_db()


def test_user_content_delete_excludes_other_users_watched_threads(
    user, other_user, thread, watched_thread_factory
):
    watched_thread = watched_thread_factory(other_user, thread, send_emails=True)

    user.delete_content()

    watched_thread.refresh_from_db()
