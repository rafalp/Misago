from django.urls import reverse

from ...privatethreads.models import PrivateThreadMember
from ...test import assert_contains
from ..enums import NotificationVerb
from ..models import Notification
from ..registry import registry


def test_notification_view_returns_redirect_to_user_notification(rf, user, user_client):
    request = rf.get("/notification/1/")
    notification = Notification.objects.create(user=user, verb="TEST")
    response = user_client.get(
        reverse("misago:notification", kwargs={"notification_id": notification.id})
    )
    assert response.status_code == 302
    assert response.headers["location"] == registry.get_redirect_url(
        request, notification
    )


def test_notification_view_sets_notification_as_read(user, user_client):
    notification = Notification.objects.create(user=user, verb="TEST", is_read=False)
    response = user_client.get(
        reverse("misago:notification", kwargs={"notification_id": notification.id})
    )
    assert response.status_code == 302

    notification.refresh_from_db()
    assert notification.is_read


def test_notification_view_updates_user_unread_notifications_count(user, user_client):
    user.unread_notifications = 1
    user.save()

    notification = Notification.objects.create(user=user, verb="TEST", is_read=False)
    response = user_client.get(
        reverse("misago:notification", kwargs={"notification_id": notification.id})
    )
    assert response.status_code == 302

    user.refresh_from_db()
    assert user.unread_notifications == 0


def test_notification_view_skips_user_unread_notifications_count_for_read_notification(
    user, user_client
):
    user.unread_notifications = 1
    user.save()

    notification = Notification.objects.create(user=user, verb="TEST", is_read=True)
    response = user_client.get(
        reverse("misago:notification", kwargs={"notification_id": notification.id})
    )
    assert response.status_code == 302

    user.refresh_from_db()
    assert user.unread_notifications == 1


def test_notification_view_returns_404_error_for_nonexisting_notification(user_client):
    response = user_client.get(
        reverse("misago:notification", kwargs={"notification_id": 1})
    )
    assert response.status_code == 404


def test_notification_view_returns_404_error_for_other_user_notification(
    other_user, user_client
):
    notification = Notification.objects.create(user=other_user, verb="TEST")
    response = user_client.get(
        reverse("misago:notification", kwargs={"notification_id": notification.id})
    )
    assert response.status_code == 404


def test_notification_view_returns_404_error_for_unsupported_verb_notification(
    user, user_client
):
    notification = Notification.objects.create(user=user, verb="REMOVED")
    response = user_client.get(
        reverse("misago:notification", kwargs={"notification_id": notification.id})
    )
    assert response.status_code == 404


def test_notification_view_shows_permission_denied_page_to_anonymous_users(db, client):
    response = client.get(reverse("misago:notification", kwargs={"notification_id": 1}))
    assert_contains(response, "You must be signed in", status_code=403)


def test_notification_view_returns_redirect_to_thread_reply(
    user, user_client, default_category, thread, other_user_reply
):
    notification = Notification.objects.create(
        user=user,
        verb=NotificationVerb.REPLIED_TO_THREAD,
        category=default_category,
        thread=thread,
        thread_title=thread.title,
        post=other_user_reply,
    )

    response = user_client.get(
        reverse("misago:notification", kwargs={"notification_id": notification.id})
    )
    assert response.status_code == 302
    assert response.headers["location"]


def test_notification_view_returns_redirect_to_private_thread_reply(
    user, user_client, private_threads_category, private_thread, private_thread_reply
):
    PrivateThreadMember.objects.create(thread=private_thread, user=user)

    notification = Notification.objects.create(
        user=user,
        verb=NotificationVerb.REPLIED_TO_THREAD,
        category=private_threads_category,
        thread=private_thread,
        thread_title=private_thread.title,
        post=private_thread_reply,
    )

    response = user_client.get(
        reverse("misago:notification", kwargs={"notification_id": notification.id})
    )
    assert response.status_code == 302
    assert response.headers["location"]


def test_notification_view_returns_redirect_to_private_thread(
    user, user_client, private_threads_category, private_thread
):
    PrivateThreadMember.objects.create(thread=private_thread, user=user)

    notification = Notification.objects.create(
        user=user,
        verb=NotificationVerb.ADDED_TO_PRIVATE_THREAD,
        category=private_threads_category,
        thread=private_thread,
        thread_title=private_thread.title,
        post_id=private_thread.first_post_id,
    )

    response = user_client.get(
        reverse("misago:notification", kwargs={"notification_id": notification.id})
    )
    assert response.status_code == 302
    assert response.headers["location"]
