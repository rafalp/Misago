from django.urls import reverse

from ...test import assert_contains, assert_not_contains


def test_select_user_view_returns_empty_message_if_query_is_not_set(admin_client):
    response = admin_client.get(reverse("misago:admin:select-user"))
    assert_contains(response, "Enter a user name to search.")


def test_select_user_view_returns_empty_message_if_query_has_no_results(admin_client):
    response = admin_client.get(reverse("misago:admin:select-user") + "?search=blank")
    assert_contains(response, "No matching users have been found.")


def test_select_user_view_returns_exact_results(admin_client, admin):
    response = admin_client.get(reverse("misago:admin:select-user") + "?search=admin")
    assert_contains(response, admin.username)


def test_select_user_view_returns_results_matching_prefix(admin_client, admin):
    response = admin_client.get(reverse("misago:admin:select-user") + "?search=ad")
    assert_contains(response, admin.username)


def test_select_user_view_returns_excludes_users_not_matching_query(
    admin_client, admin, other_user
):
    response = admin_client.get(reverse("misago:admin:select-user") + "?search=other")
    assert_contains(response, other_user.username)
    assert_not_contains(response, admin.username)


def test_select_user_view_requires_admin_auth(user_client):
    response = user_client.get(reverse("misago:admin:select-user"))
    assert response.status_code == 302
