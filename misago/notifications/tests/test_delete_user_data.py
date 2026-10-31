import pytest

from misago.users.delete import delete_user_content
from ..models import Notification, WatchedThread


def test_user_content_delete_deletes_user_notifications(user, other_user):
    notification = Notification.objects.create(
        user=user,
        actor=other_user,
        actor_name=other_user.username,
        verb="TEST",
    )

    delete_user_content(user)

    with pytest.raises(Notification.DoesNotExist):
        notification.refresh_from_db()


def test_user_content_delete_deletes_actor_notifications(user, other_user):
    notification = Notification.objects.create(
        user=user,
        actor=other_user,
        actor_name=other_user.username,
        verb="TEST",
    )

    delete_user_content(other_user)

    with pytest.raises(Notification.DoesNotExist):
        notification.refresh_from_db()


def test_user_content_delete_excludes_other_users_notifications(user, other_user):
    notification = Notification.objects.create(
        user=other_user,
        verb="TEST",
    )

    delete_user_content(user)

    notification.refresh_from_db()


def test_user_content_delete_deletes_users_watched_threads(
    watched_thread_factory, user, old_thread
):
    watched_thread = watched_thread_factory(user, old_thread, send_emails=True)

    delete_user_content(user)

    with pytest.raises(WatchedThread.DoesNotExist):
        watched_thread.refresh_from_db()


def test_user_content_delete_excludes_other_users_watched_threads(
    watched_thread_factory, user, other_user, old_thread
):
    watched_thread = watched_thread_factory(other_user, old_thread, send_emails=True)

    delete_user_content(user)

    watched_thread.refresh_from_db()
