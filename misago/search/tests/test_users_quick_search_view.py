import json

from django.urls import reverse

from ...test import assert_contains, assert_not_contains


def test_users_quick_search_view_returns_error_404_if_request_is_not_htmx(
    user_client, user
):
    user.group.can_search = False
    user.group.save()

    response = user_client.get(reverse("misago:users-quick-search"))
    assert response.status_code == 404


def test_users_quick_search_view_returns_error_403_if_user_cant_search(
    user_client, user
):
    user.group.can_search = False
    user.group.save()

    response = user_client.get(
        reverse("misago:users-quick-search"), headers={"hx-request": "true"}
    )

    assert response.status_code == 403
    assert json.loads(response.content) == {"error": "You can't search this site."}


def test_users_quick_search_view_returns_error_403_if_user_cant_search_users(
    user_client, user
):
    user.group.can_search_users = False
    user.group.save()

    response = user_client.get(
        reverse("misago:users-quick-search"), headers={"hx-request": "true"}
    )

    assert response.status_code == 403
    assert json.loads(response.content) == {"error": "You can't search for users."}


def test_users_quick_search_view_shows_search_result(user_client, other_user):
    response = user_client.get(
        reverse("misago:users-quick-search") + f"?query={other_user.username}",
        headers={"hx-request": "true"},
    )

    assert_contains(response, other_user.username)
    assert_contains(
        response,
        reverse(
            "misago:user", kwargs={"user_id": other_user.id, "slug": other_user.slug}
        ),
    )
    assert_not_contains(response, "No users found")


def test_users_quick_search_view_shows_search_result_with_group(
    user_client, members_group, other_user
):
    members_group.is_page = True
    members_group.is_hidden = False
    members_group.color = "#ff0000"
    members_group.save()

    response = user_client.get(
        reverse("misago:users-quick-search") + f"?query={other_user.username}",
        headers={"hx-request": "true"},
    )

    assert_contains(response, other_user.username)
    assert_contains(
        response,
        reverse(
            "misago:user", kwargs={"user_id": other_user.id, "slug": other_user.slug}
        ),
    )
    assert_contains(response, members_group.name)
    assert_not_contains(response, "No users found")


def test_users_quick_search_view_shows_search_result_with_stats(
    user_client, other_user
):
    other_user.threads = 21
    other_user.posts = 15
    other_user.save()

    response = user_client.get(
        reverse("misago:users-quick-search") + f"?query={other_user.username}",
        headers={"hx-request": "true"},
    )

    assert_contains(response, other_user.username)
    assert_contains(
        response,
        reverse(
            "misago:user", kwargs={"user_id": other_user.id, "slug": other_user.slug}
        ),
    )
    assert_not_contains(response, "No users found")


def test_users_quick_search_view_shows_no_results_page(user_client):
    response = user_client.get(
        reverse("misago:users-quick-search") + f"?query=nothing",
        headers={"hx-request": "true"},
    )

    assert_contains(response, "No users found")
