from django.urls import reverse

from ...test import assert_contains, assert_not_contains


def test_quick_search_is_available_if_user_has_permission(user_client):
    response = user_client.get(reverse("misago:index"))
    assert_contains(response, "misago-quick-search")


def test_quick_search_is_available_if_anonymous_user_has_permission(db, client):
    response = client.get(reverse("misago:index"))
    assert_contains(response, "misago-quick-search")


def test_quick_search_is_not_available_if_user_cant_search(user_client, user):
    user.group.can_search = False
    user.group.save()

    response = user_client.get(reverse("misago:index"))
    assert_not_contains(response, "misago-quick-search")


def test_quick_search_is_not_available_if_anonymous_user_cant_search(
    client, guests_group
):
    guests_group.can_search = False
    guests_group.save()

    response = client.get(reverse("misago:index"))
    assert_not_contains(response, "misago-quick-search")


def test_quick_search_includes_threads_for_user(user_client):
    response = user_client.get(reverse("misago:index"))
    assert_contains(response, "misago-quick-search")
    assert_contains(response, reverse("misago:threads-quick-search"))


def test_quick_search_includes_threads_for_anonymous_user(db, user_client):
    response = user_client.get(reverse("misago:index"))
    assert_contains(response, "misago-quick-search")
    assert_contains(response, reverse("misago:threads-quick-search"))


def test_quick_search_includes_private_threads_if_user_has_permission(user_client):
    response = user_client.get(reverse("misago:index"))
    assert_contains(response, "misago-quick-search")
    assert_contains(response, reverse("misago:private-threads-quick-search"))


def test_quick_search_excludes_private_threads_if_user_doesnt_have_permission(
    user_client, user
):
    user.group.can_use_private_threads = False
    user.group.save()

    response = user_client.get(reverse("misago:index"))
    assert_contains(response, "misago-quick-search")
    assert_not_contains(response, reverse("misago:private-threads-quick-search"))


def test_quick_search_excludes_private_threads_for_anonymous_user(db, client):
    response = client.get(reverse("misago:index"))
    assert_contains(response, "misago-quick-search")
    assert_not_contains(response, reverse("misago:private-threads-quick-search"))


def test_quick_search_includes_users_if_user_has_permission(user_client):
    response = user_client.get(reverse("misago:index"))
    assert_contains(response, "misago-quick-search")
    assert_contains(response, reverse("misago:users-quick-search"))


def test_quick_search_excludes_users_if_user_doesnt_have_permission(user_client, user):
    user.group.can_search_users = False
    user.group.save()

    response = user_client.get(reverse("misago:index"))
    assert_contains(response, "misago-quick-search")
    assert_not_contains(response, reverse("misago:users-quick-search"))


def test_quick_search_includes_users_if_anonymous_user_has_permission(db, client):
    response = client.get(reverse("misago:index"))
    assert_contains(response, "misago-quick-search")
    assert_contains(response, reverse("misago:users-quick-search"))


def test_quick_search_excludes_users_if_anonymous_user_doesnt_have_permission(
    client, guests_group
):
    guests_group.can_search_users = False
    guests_group.save()

    response = client.get(reverse("misago:index"))
    assert_contains(response, "misago-quick-search")
    assert_not_contains(response, reverse("misago:users-quick-search"))
