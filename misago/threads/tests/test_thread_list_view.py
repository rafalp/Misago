from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...test import assert_contains


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_renders_empty_to_guests(db, client):
    response = client.get(reverse("misago:thread-list"))
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_renders_empty_to_users(user_client):
    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_renders_empty_to_global_moderators(moderator_client):
    response = moderator_client.get(reverse("misago:thread-list"))
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_renders_empty_to_guests_in_htmx(db, client):
    response = client.get(reverse("misago:thread-list"), headers={"hx-request": "true"})
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_renders_empty_to_users_in_htmx(user_client):
    response = user_client.get(
        reverse("misago:thread-list"), headers={"hx-request": "true"}
    )
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_renders_empty_to_global_moderators_in_htmx(moderator_client):
    response = moderator_client.get(
        reverse("misago:thread-list"), headers={"hx-request": "true"}
    )
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="threads")
def test_thread_list_view_on_site_index_renders_empty_to_guests(db, client):
    response = client.get(reverse("misago:index"))
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="threads")
def test_thread_list_view_on_site_index_renders_empty_to_users(user_client):
    response = user_client.get(reverse("misago:index"))
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="threads")
def test_thread_list_view_on_site_index_renders_empty_to_global_moderators(
    moderator_client,
):
    response = moderator_client.get(reverse("misago:index"))
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="threads")
def test_thread_list_view_on_site_index_renders_empty_to_guests_in_htmx(db, client):
    response = client.get(reverse("misago:index"), headers={"hx-request": "true"})
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="threads")
def test_thread_list_view_on_site_index_renders_empty_to_users_in_htmx(user_client):
    response = user_client.get(reverse("misago:index"), headers={"hx-request": "true"})
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="threads")
def test_thread_list_view_on_site_index_renders_empty_to_global_moderators_in_htmx(
    moderator_client,
):
    response = moderator_client.get(
        reverse("misago:index"), headers={"hx-request": "true"}
    )
    assert_contains(response, "No threads have been started yet")
