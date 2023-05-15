from django.urls import reverse

from ....notifications.models import Notification


def test_notifications_read_all_api_returns_403_error_if_client_is_no_authenticated(
    db, client
):
    response = client.post(reverse("misago:apiv2:notifications-read-all"))
    assert response.status_code == 403


def test_notifications_read_all_api_marks_users_notifications_as_read(
    user, user_client
):
    notification = Notification.objects.create(user=user, verb="TEST", is_read=False)

    user.unread_notifications = 10
    user.save()

    response = user_client.post(reverse("misago:apiv2:notifications-read-all"))
    assert response.status_code == 204

    notification.refresh_from_db()
    assert notification.is_read

    # User unread notifications counter is zeroed
    user.refresh_from_db()
    assert user.unread_notifications == 0


def test_notifications_read_all_api_excludes_other_users_notifications(
    other_user, user_client
):
    notification = Notification.objects.create(
        user=other_user, verb="TEST", is_read=False
    )

    other_user.unread_notifications = 10
    other_user.save()

    response = user_client.post(reverse("misago:apiv2:notifications-read-all"))
    assert response.status_code == 204

    notification.refresh_from_db()
    assert not notification.is_read

    other_user.refresh_from_db()
    assert other_user.unread_notifications == 10


def test_notifications_read_all_api_works_when_user_has_no_unread_notifications(
    user, user_client
):
    notification = Notification.objects.create(user=user, verb="TESt", is_read=True)

    user.unread_notifications = 0
    user.save()

    response = user_client.post(reverse("misago:apiv2:notifications-read-all"))
    assert response.status_code == 204

    notification.refresh_from_db()
    assert notification.is_read

    # User unread notifications counter is zeroed
    user.refresh_from_db()
    assert user.unread_notifications == 0


def test_notifications_read_all_api_works_when_user_has_no_notifications(
    user, user_client
):
    user.unread_notifications = 0
    user.save()

    response = user_client.post(reverse("misago:apiv2:notifications-read-all"))
    assert response.status_code == 204

    # User unread notifications counter is zeroed
    user.refresh_from_db()
    assert user.unread_notifications == 0
