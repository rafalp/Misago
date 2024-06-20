from django.urls import reverse

from ...test import assert_contains


def test_site_threads_list_renders_empty_to_guests(db, client):
    response = client.get(reverse("misago:threads"))
    assert response.status_code == 200


def test_site_threads_list_renders_empty_to_users(user_client):
    response = user_client.get(reverse("misago:threads"))
    assert response.status_code == 200


def test_site_threads_list_renders_empty_to_moderators(moderator_client):
    response = moderator_client.get(reverse("misago:threads"))
    assert response.status_code == 200


def test_category_threads_list_renders_empty_to_guests(default_category, client):
    response = client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)


def test_category_threads_list_renders_empty_to_users(default_category, user_client):
    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)


def test_category_threads_list_renders_empty_to_moderators(
    default_category, moderator_client
):
    response = moderator_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)


def test_child_category_threads_list_renders_empty_to_guests(child_category, client):
    response = client.get(child_category.get_absolute_url())
    assert_contains(response, child_category.name)


def test_child_category_threads_list_renders_empty_to_users(
    child_category, user_client
):
    response = user_client.get(child_category.get_absolute_url())
    assert_contains(response, child_category.name)


def test_child_category_threads_list_renders_empty_to_moderators(
    child_category, moderator_client
):
    response = moderator_client.get(child_category.get_absolute_url())
    assert_contains(response, child_category.name)


def test_hidden_category_threads_list_renders_error_to_guests(hidden_category, client):
    response = client.get(hidden_category.get_absolute_url())
    assert response.status_code == 404


def test_hidden_category_threads_list_renders_error_to_users(
    hidden_category, user_client
):
    response = user_client.get(hidden_category.get_absolute_url())
    assert response.status_code == 404


def test_private_threads_list_shows_permission_error_to_guests(db, client):
    response = client.get(reverse("misago:private-threads"))
    assert_contains(
        response, "You must be signed in to use private threads.", status_code=403
    )


def test_private_threads_list_renders_empty_to_users(user_client):
    response = user_client.get(reverse("misago:private-threads"))
    assert_contains(response, "Private threads")


def test_private_threads_list_shows_permission_error_to_users_without_permission(
    user_client, members_group
):
    members_group.can_use_private_threads = False
    members_group.save()

    response = user_client.get(reverse("misago:private-threads"))
    print(response.content)
    assert_contains(response, "You can&#x27;t use private threads.", status_code=403)


def test_private_threads_list_renders_empty_to_moderators(moderator_client):
    response = moderator_client.get(reverse("misago:private-threads"))
    assert_contains(response, "Private threads")
