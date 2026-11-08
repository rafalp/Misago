from django.urls import reverse

from ...permissions.enums import PermissionValue
from ...test import assert_contains, assert_not_contains


def test_search_view(user_client):
    response = user_client.get(reverse("misago:search"))
    assert_contains(response, reverse("misago:threads-search"))


def test_search_view_returns_error_403_if_user_has_no_permission(
    user_client, members_group
):
    members_group.can_search = PermissionValue.NO
    members_group.save()

    response = user_client.get(reverse("misago:search"))
    assert response.status_code == 403


def test_search_view_includes_private_threads_if_user_has_permission(
    user_client, members_group
):
    response = user_client.get(reverse("misago:search"))
    assert_contains(response, reverse("misago:private-threads-search"))


def test_search_view_excludes_private_threads_if_user_has_no_permission(
    user_client, members_group
):
    members_group.can_use_private_threads = PermissionValue.NO
    members_group.save()

    response = user_client.get(reverse("misago:search"))
    assert_not_contains(response, reverse("misago:private-threads-search"))


def test_search_view_includes_users_if_user_has_permission(user_client, members_group):
    response = user_client.get(reverse("misago:search"))
    assert_contains(response, reverse("misago:users-search"))


def test_search_view_excludes_users_if_user_has_no_permission(
    user_client, members_group
):
    members_group.can_search_users = PermissionValue.NO
    members_group.save()

    response = user_client.get(reverse("misago:search"))
    assert_not_contains(response, reverse("misago:users-search"))
