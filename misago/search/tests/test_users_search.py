from django.urls import reverse

from ...test import assert_contains, assert_not_contains


def test_users_search_view_returns_error_403_if_user_cant_search(user_client, user):
    user.group.can_search = False
    user.group.save()

    response = user_client.get(reverse("misago:users-search"))
    assert_contains(response, "You can&#x27;t search this site.", status_code=403)


def test_users_search_view_returns_error_403_if_user_cant_search_users(
    user_client, user
):
    user.group.can_search_users = False
    user.group.save()

    response = user_client.get(reverse("misago:users-search"))
    assert_contains(response, "You can&#x27;t search for users.", status_code=403)


def test_threads_search_view_shows_search_result(user_client, other_user):
    response = user_client.get(
        reverse("misago:users-search") + f"?query={other_user.username}"
    )

    assert_contains(response, "Search users")
    assert_contains(response, other_user.username)
    assert_contains(
        response,
        reverse(
            "misago:user", kwargs={"user_id": other_user.id, "slug": other_user.slug}
        ),
    )
    assert_not_contains(response, "No users found")


def test_threads_search_view_shows_search_result_with_group(
    user_client, members_group, other_user
):
    members_group.is_page = True
    members_group.is_hidden = False
    members_group.color = "#ff0000"
    members_group.save()

    response = user_client.get(
        reverse("misago:users-search") + f"?query={other_user.username}"
    )

    assert_contains(response, "Search users")
    assert_contains(response, other_user.username)
    assert_contains(
        response,
        reverse(
            "misago:user", kwargs={"user_id": other_user.id, "slug": other_user.slug}
        ),
    )
    assert_not_contains(response, "No users found")


def test_threads_search_view_shows_search_result_with_stats(user_client, other_user):
    other_user.threads = 21
    other_user.posts = 15
    other_user.save()

    response = user_client.get(
        reverse("misago:users-search") + f"?query={other_user.username}"
    )

    assert_contains(response, "Search users")
    assert_contains(response, other_user.username)
    assert_contains(
        response,
        reverse(
            "misago:user", kwargs={"user_id": other_user.id, "slug": other_user.slug}
        ),
    )
    assert_not_contains(response, "No users found")


def test_threads_search_view_shows_no_results_page(user_client):
    response = user_client.get(reverse("misago:users-search") + f"?query=nothing")

    assert_contains(response, "Search users")
    assert_contains(response, "No users found")
