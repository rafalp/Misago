from django.urls import reverse

from ...test import assert_contains
from ..models import Notification
from ..redirects import redirect_factory


def test_notification_view_returns_redirect_to_user_notification(user, user_client):
    notification = Notification.objects.create(user=user, verb="test")
    response = user_client.get(
        reverse("misago:notification", kwargs={"notification_id": notification.id})
    )
    assert response.status_code == 302
    assert response.headers["location"] == redirect_factory.get_redirect_url(
        notification
    )


def test_notification_view_sets_notification_as_read(user, user_client):
    notification = Notification.objects.create(user=user, verb="test", is_read=False)
    response = user_client.get(
        reverse("misago:notification", kwargs={"notification_id": notification.id})
    )
    assert response.status_code == 302

    notification.refresh_from_db()
    assert notification.is_read


def test_notification_view_updates_user_unread_notifications_count(user, user_client):
    user.unread_notifications = 1
    user.save()

    notification = Notification.objects.create(user=user, verb="test", is_read=False)
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

    notification = Notification.objects.create(user=user, verb="test", is_read=True)
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
    notification = Notification.objects.create(user=other_user, verb="test")
    response = user_client.get(
        reverse("misago:notification", kwargs={"notification_id": notification.id})
    )
    assert response.status_code == 404


def test_notification_view_shows_permission_denied_page_to_guests(db, client):
    response = client.get(reverse("misago:notification", kwargs={"notification_id": 1}))
    assert_contains(response, "You must be signed in", status_code=403)
