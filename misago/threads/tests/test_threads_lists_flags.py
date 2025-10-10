from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...test import assert_contains, assert_not_contains


@override_dynamic_settings(index_view="categories")
def test_site_threads_list_shows_thread_globally_pinned_flag(
    thread_factory, default_category, client
):
    thread = thread_factory(default_category, weight=2)

    response = client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-pinned-globally")


def test_category_threads_list_shows_thread_globally_pinned_flag(
    thread_factory, default_category, client
):
    thread = thread_factory(default_category, title="Global Thread", weight=2)

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-pinned-globally")


@override_dynamic_settings(index_view="categories")
def test_site_threads_list_doesnt_show_users_thread_ghost_pinned_flag(
    thread_factory, default_category, user_client
):
    thread = thread_factory(default_category, weight=1)

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")
    assert_not_contains(response, "thread-flag-pinned-locally")


def test_category_threads_list_doesnt_show_users_ghost_thread_ghost_pinned_flag(
    thread_factory, default_category, child_category, user_client
):
    thread = thread_factory(child_category, weight=1)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")
    assert_not_contains(response, "thread-flag-pinned-locally")


@override_dynamic_settings(index_view="categories")
def test_site_threads_list_shows_moderators_thread_ghost_pinned_flag(
    thread_factory, default_category, moderator_client
):
    thread = thread_factory(default_category, weight=1)

    response = moderator_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-pinned-locally-elsewhere")


def test_category_threads_list_shows_moderators_thread_ghost_pinned_flag(
    thread_factory, default_category, child_category, moderator_client
):
    thread = thread_factory(child_category, weight=1)

    response = moderator_client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-pinned-locally-elsewhere")


def test_category_threads_list_shows_thread_pinned_flag(
    thread_factory, default_category, moderator_client
):
    thread = thread_factory(default_category, weight=1)

    response = moderator_client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-pinned-locally")


@override_dynamic_settings(index_view="categories")
def test_site_threads_list_doesnt_show_thread_pinned_flag_for_unpinned_thread(
    thread_factory, default_category, client
):
    thread = thread_factory(default_category)

    response = client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")
    assert_not_contains(response, "thread-flag-pinned")


def test_category_threads_list_shows_thread_globally_pinned_flag(
    thread_factory, default_category, client
):
    thread = thread_factory(default_category)

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")
    assert_not_contains(response, "thread-flag-pinned")


@override_dynamic_settings(index_view="categories")
def test_site_threads_list_shows_moderators_thread_has_unapproved_posts_flag(
    thread_factory, default_category, moderator_client
):
    thread = thread_factory(default_category, has_unapproved_posts=True)

    response = moderator_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-unapproved")


def test_category_threads_list_shows_moderators_thread_has_unapproved_posts_flag(
    thread_factory, default_category, moderator_client
):
    thread = thread_factory(default_category, has_unapproved_posts=True)

    response = moderator_client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-unapproved")


@override_dynamic_settings(index_view="categories")
def test_site_threads_list_shows_moderators_thread_is_unapproved_flag(
    thread_factory, default_category, moderator_client
):
    thread = thread_factory(default_category, is_unapproved=True)

    response = moderator_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-unapproved")


def test_category_threads_list_shows_moderators_thread_is_unapproved_flag(
    thread_factory, default_category, moderator_client
):
    thread = thread_factory(default_category, is_unapproved=True)

    response = moderator_client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-unapproved")


@override_dynamic_settings(index_view="categories")
def test_site_threads_list_shows_moderators_thread_has_unapproved_posts_flag(
    thread_factory, default_category, moderator_client
):
    thread = thread_factory(default_category, has_unapproved_posts=True)

    response = moderator_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-unapproved")


def test_category_threads_list_shows_moderators_thread_has_unapproved_posts_flag(
    thread_factory, default_category, moderator_client
):
    thread = thread_factory(default_category, has_unapproved_posts=True)

    response = moderator_client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-unapproved")


@override_dynamic_settings(index_view="categories")
def test_site_threads_list_doesnt_show_user_thread_has_unapproved_posts_flag(
    thread_factory, default_category, user_client
):
    thread = thread_factory(default_category, has_unapproved_posts=True)

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")
    assert_not_contains(response, "thread-flag-unapproved")


def test_category_threads_list_doesnt_show_user_thread_has_unapproved_posts_flag(
    thread_factory, default_category, user_client
):
    thread = thread_factory(default_category, has_unapproved_posts=True)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")
    assert_not_contains(response, "thread-flag-unapproved")
