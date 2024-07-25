from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...test import assert_contains, assert_not_contains
from ..test import post_thread


@override_dynamic_settings(index_view="categories")
def test_site_threads_list_renders_thread_globally_pinned_flag(
    default_category, client
):
    thread = post_thread(default_category, title="Global Thread", is_global=True)

    response = client.get(reverse("misago:threads"))
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flag-pinned-globally")


def test_category_threads_list_renders_thread_globally_pinned_flag(
    default_category, client
):
    thread = post_thread(default_category, title="Global Thread", is_global=True)

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flag-pinned-globally")


@override_dynamic_settings(index_view="categories")
def test_site_threads_list_hides_thread_ghost_pinned_flag_from_users(
    default_category, user_client
):
    thread = post_thread(default_category, title="Pinned Thread", is_pinned=True)

    response = user_client.get(reverse("misago:threads"))
    assert_contains(response, thread.title)
    assert_not_contains(response, "thread-flag-pinned-locally")


def test_category_threads_list_hides_ghost_thread_ghost_pinned_flag_from_users(
    default_category, child_category, user_client
):
    thread = post_thread(child_category, title="Pinned Thread", is_pinned=True)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)
    assert_not_contains(response, "thread-flag-pinned-locally")


@override_dynamic_settings(index_view="categories")
def test_site_threads_list_renders_moderator_thread_ghost_pinned_flag(
    default_category, moderator_client
):
    thread = post_thread(default_category, title="Pinned Thread", is_pinned=True)

    response = moderator_client.get(reverse("misago:threads"))
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flag-pinned-locally-elsewhere")


def test_category_threads_list_renders_moderator_thread_ghost_pinned_flag(
    default_category, child_category, moderator_client
):
    thread = post_thread(child_category, title="Pinned Thread", is_pinned=True)

    response = moderator_client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flag-pinned-locally-elsewhere")


def test_category_threads_list_renders_thread_pinned_flag(
    default_category, moderator_client
):
    thread = post_thread(default_category, title="Pinned Thread", is_pinned=True)

    response = moderator_client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flag-pinned-locally")


@override_dynamic_settings(index_view="categories")
def test_site_threads_list_doesnt_render_thread_pinned_flag_for_unpinned_thread(
    default_category, client
):
    thread = post_thread(default_category, title="Regular Thread")

    response = client.get(reverse("misago:threads"))
    assert_contains(response, thread.title)
    assert_not_contains(response, "thread-flag-pinned")


def test_category_threads_list_renders_thread_globally_pinned_flag(
    default_category, client
):
    thread = post_thread(default_category, title="Regular Thread")

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)
    assert_not_contains(response, "thread-flag-pinned")
