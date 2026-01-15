from django.urls import reverse

from ...test import assert_contains


def test_notifications_view_is_accessible_by_users(user_client):
    response = user_client.get(reverse("misago:notifications"))
    assert_contains(response, "Notifications")
    assert_contains(response, "enable JavaScript")


def test_notifications_view_shows_permission_denied_page_to_anonymous_users(db, client):
    response = client.get(reverse("misago:notifications"))
    assert_contains(response, "You must be signed in", status_code=403)
