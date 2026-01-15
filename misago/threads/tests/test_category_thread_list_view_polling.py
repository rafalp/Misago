from django.urls import reverse

from ...categories.models import Category
from ...conf.test import override_dynamic_settings
from ...test import assert_contains, assert_not_contains
from ..enums import ThreadsListsPolling


def test_category_thread_list_view_includes_polling_if_its_not_empty(
    thread_factory, client, default_category
):
    thread = thread_factory(default_category)

    response = client.get(default_category.get_absolute_url())
    assert_contains(
        response,
        default_category.get_absolute_url() + f"?poll_new={thread.last_post_id}",
    )


@override_dynamic_settings(threads_lists_polling=ThreadsListsPolling.DISABLED)
def test_category_thread_list_view_excludes_polling_for_anonymous_users_if_its_disabled(
    thread_factory, client, default_category
):
    thread_factory(default_category)

    response = client.get(default_category.get_absolute_url())
    assert_not_contains(response, default_category.get_absolute_url() + "?poll_new=")


@override_dynamic_settings(threads_lists_polling=ThreadsListsPolling.DISABLED)
def test_category_thread_list_view_excludes_polling_for_authenticated_if_its_disabled(
    thread_factory, user_client, default_category
):
    thread_factory(default_category)

    response = user_client.get(default_category.get_absolute_url())
    assert_not_contains(response, default_category.get_absolute_url() + "?poll_new=")


@override_dynamic_settings(threads_lists_polling=ThreadsListsPolling.ENABLED_FOR_USERS)
def test_category_thread_list_view_excludes_polling_for_guest_if_its_enabled_for_users(
    thread_factory, client, default_category
):
    thread_factory(default_category)

    response = client.get(default_category.get_absolute_url())
    assert_not_contains(response, default_category.get_absolute_url() + "?poll_new=")


@override_dynamic_settings(threads_lists_polling=ThreadsListsPolling.ENABLED_FOR_USERS)
def test_category_thread_list_view_includes_polling_for_user_if_its_enabled_for_users(
    thread_factory, user_client, default_category
):
    thread = thread_factory(default_category)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(
        response,
        default_category.get_absolute_url() + f"?poll_new={thread.last_post_id}",
    )


def test_category_thread_list_view_poll_returns_update_button_for_hx_request_if_there_are_new_threads(
    thread_factory, client, default_category
):
    thread_factory(default_category)
    thread_factory(default_category)

    response = client.get(
        default_category.get_absolute_url() + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Show 2 new or updated threads")


def test_category_thread_list_view_poll_returns_update_button_for_hx_request_if_there_are_new_threads_after_thread(
    thread_factory, client, default_category
):
    thread = thread_factory(default_category)
    thread_factory(default_category)
    thread_factory(default_category)

    response = client.get(
        default_category.get_absolute_url() + f"?poll_new={thread.last_post_id}",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Show 2 new or updated threads")


def test_category_thread_list_view_poll_doesnt_return_update_button_for_hx_request_if_there_are_no_new_threads(
    client, default_category
):
    response = client.get(
        default_category.get_absolute_url() + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "new or updated thread")


def test_category_thread_list_view_poll_doesnt_return_update_button_for_hx_request_if_there_are_no_new_threads_after_thread(
    thread_factory, client, default_category
):
    thread = thread_factory(default_category)
    response = client.get(
        default_category.get_absolute_url() + f"?poll_new={thread.last_post_id}",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "new or updated thread")


@override_dynamic_settings(threads_lists_polling=ThreadsListsPolling.DISABLED)
def test_category_thread_list_view_poll_doesnt_return_update_button_for_guest_hx_request_if_polling_is_disabled(
    thread_factory, client, default_category
):
    thread_factory(default_category)
    thread_factory(default_category)

    response = client.get(
        default_category.get_absolute_url() + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "new or updated thread")


@override_dynamic_settings(threads_lists_polling=ThreadsListsPolling.DISABLED)
def test_category_thread_list_view_poll_doesnt_return_update_button_for_user_hx_request_if_polling_is_disabled(
    thread_factory, client, default_category
):
    thread_factory(default_category)
    thread_factory(default_category)

    response = client.get(
        default_category.get_absolute_url() + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "new or updated thread")


@override_dynamic_settings(threads_lists_polling=ThreadsListsPolling.ENABLED_FOR_USERS)
def test_category_thread_list_view_poll_doesnt_return_update_button_for_guest_hx_request_if_polling_is_disabled_for_anonymous(
    thread_factory, client, default_category
):
    thread_factory(default_category)
    thread_factory(default_category)

    response = client.get(
        default_category.get_absolute_url() + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "new or updated thread")


@override_dynamic_settings(threads_lists_polling=ThreadsListsPolling.ENABLED_FOR_USERS)
def test_category_thread_list_view_poll_returns_update_button_for_user_hx_request_if_polling_is_disabled_for_anonymous(
    thread_factory, user_client, default_category
):
    thread_factory(default_category)
    thread_factory(default_category)

    response = user_client.get(
        default_category.get_absolute_url() + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Show 2 new or updated threads")


def test_category_thread_list_view_poll_doesnt_return_button_if_request_is_not_htmx(
    thread_factory, client, default_category
):
    thread_factory(default_category)
    thread_factory(default_category)

    response = client.get(default_category.get_absolute_url() + "?poll_new=0")
    assert_not_contains(response, "Show 2 new or updated threads")


def test_category_thread_list_view_poll_uses_category_permissions(
    thread_factory, client, default_category
):
    thread_factory(default_category)

    category = Category(name="Hidden Child", slug="hidden-child")
    category.insert_at(default_category, position="last-child", save=True)

    response = client.get(
        default_category.get_absolute_url() + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Show 1 new or updated thread")


def test_category_thread_list_view_poll_raises_404_error_if_filter_is_invalid(
    thread_factory, default_category, user, user_client
):
    thread_factory(default_category, starter=user)
    response = user_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={
                "category_id": default_category.id,
                "slug": default_category.slug,
                "filter": "invalid",
            },
        )
        + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


def test_category_thread_list_view_poll_filters_threads(
    thread_factory, default_category, user, user_client
):
    thread_factory(default_category, starter=user)
    thread_factory(default_category)

    response = user_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={
                "category_id": default_category.id,
                "slug": default_category.slug,
                "filter": "my",
            },
        )
        + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Show 1 new or updated thread")
