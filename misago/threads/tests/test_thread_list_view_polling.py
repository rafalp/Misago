from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...test import assert_contains, assert_not_contains
from ..enums import ThreadsListsPolling


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_includes_polling_if_its_not_empty(
    thread_factory, client, default_category
):
    thread = thread_factory(default_category)

    response = client.get(reverse("misago:thread-list"))
    assert_contains(
        response, reverse("misago:thread-list") + f"?poll_new={thread.last_post_id}"
    )


@override_dynamic_settings(
    index_view="categories", threads_lists_polling=ThreadsListsPolling.DISABLED
)
def test_thread_list_view_excludes_polling_for_anonymous_users_if_its_disabled(
    thread_factory, client, default_category
):
    thread_factory(default_category)

    response = client.get(reverse("misago:thread-list"))
    assert_not_contains(response, reverse("misago:thread-list") + "?poll_new=")


@override_dynamic_settings(
    index_view="categories", threads_lists_polling=ThreadsListsPolling.DISABLED
)
def test_thread_list_view_excludes_polling_for_authenticated_if_its_disabled(
    thread_factory, user_client, default_category
):
    thread_factory(default_category)

    response = user_client.get(reverse("misago:thread-list"))
    assert_not_contains(response, reverse("misago:thread-list") + "?poll_new=")


@override_dynamic_settings(
    index_view="categories", threads_lists_polling=ThreadsListsPolling.ENABLED_FOR_USERS
)
def test_thread_list_view_excludes_polling_for_anonymous_users_if_its_enabled_for_users(
    thread_factory, client, default_category
):
    thread_factory(default_category)

    response = client.get(reverse("misago:thread-list"))
    assert_not_contains(response, reverse("misago:thread-list") + "?poll_new=")


@override_dynamic_settings(
    index_view="categories", threads_lists_polling=ThreadsListsPolling.ENABLED_FOR_USERS
)
def test_thread_list_view_includes_polling_for_user_if_its_enabled_for_users(
    thread_factory, user_client, default_category
):
    thread = thread_factory(default_category)

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(
        response, reverse("misago:thread-list") + f"?poll_new={thread.last_post_id}"
    )


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_poll_returns_update_button_for_hx_request_if_there_are_new_threads(
    thread_factory, client, default_category
):
    thread_factory(default_category)
    thread_factory(default_category)

    response = client.get(
        reverse("misago:thread-list") + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Show 2 new or updated threads")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_poll_returns_update_button_for_hx_request_if_there_are_new_threads_after_thread(
    thread_factory, client, default_category
):
    thread = thread_factory(default_category)
    thread_factory(default_category)
    thread_factory(default_category)

    response = client.get(
        reverse("misago:thread-list") + f"?poll_new={thread.last_post_id}",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Show 2 new or updated threads")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_poll_doesnt_return_update_button_for_hx_request_if_there_are_no_new_threads(
    db, client
):
    response = client.get(
        reverse("misago:thread-list") + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "new or updated thread")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_poll_doesnt_return_update_button_for_hx_request_if_there_are_no_new_threads_after_thread(
    thread_factory, client, default_category
):
    thread = thread_factory(default_category)
    response = client.get(
        reverse("misago:thread-list") + f"?poll_new={thread.last_post_id}",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "new or updated thread")


@override_dynamic_settings(
    index_view="categories", threads_lists_polling=ThreadsListsPolling.DISABLED
)
def test_thread_list_view_poll_doesnt_return_update_button_for_guest_hx_request_if_polling_is_disabled(
    thread_factory, client, default_category
):
    thread_factory(default_category)
    thread_factory(default_category)

    response = client.get(
        reverse("misago:thread-list") + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "new or updated thread")


@override_dynamic_settings(
    index_view="categories", threads_lists_polling=ThreadsListsPolling.DISABLED
)
def test_thread_list_view_poll_doesnt_return_update_button_for_user_hx_request_if_polling_is_disabled(
    thread_factory, client, default_category
):
    thread_factory(default_category)
    thread_factory(default_category)

    response = client.get(
        reverse("misago:thread-list") + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "new or updated thread")


@override_dynamic_settings(
    index_view="categories", threads_lists_polling=ThreadsListsPolling.ENABLED_FOR_USERS
)
def test_thread_list_view_poll_doesnt_return_update_button_for_guest_hx_request_if_polling_is_disabled_for_anonymous(
    thread_factory, client, default_category
):
    thread_factory(default_category)
    thread_factory(default_category)

    response = client.get(
        reverse("misago:thread-list") + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "new or updated thread")


@override_dynamic_settings(
    index_view="categories", threads_lists_polling=ThreadsListsPolling.ENABLED_FOR_USERS
)
def test_thread_list_view_poll_returns_update_button_for_user_hx_request_if_polling_is_disabled_for_anonymous(
    thread_factory, user_client, default_category
):
    thread_factory(default_category)
    thread_factory(default_category)

    response = user_client.get(
        reverse("misago:thread-list") + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Show 2 new or updated threads")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_poll_doesnt_return_button_if_request_is_not_htmx(
    thread_factory, client, default_category
):
    thread_factory(default_category)
    thread_factory(default_category)

    response = client.get(reverse("misago:thread-list") + "?poll_new=0")
    assert_not_contains(response, "Show 2 new or updated threads")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_poll_uses_category_permissions(
    thread_factory, client, default_category, hidden_category
):
    thread_factory(hidden_category)
    thread_factory(default_category)

    response = client.get(
        reverse("misago:thread-list") + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Show 1 new or updated thread")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_poll_raises_404_error_if_filter_is_invalid(
    thread_factory, default_category, user, user_client
):
    thread_factory(default_category, starter=user)
    response = user_client.get(
        reverse("misago:thread-list", kwargs={"filter": "invalid"}) + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_poll_filters_threads(
    thread_factory, default_category, user, user_client
):
    thread_factory(default_category, starter=user)
    thread_factory(default_category)

    response = user_client.get(
        reverse("misago:thread-list", kwargs={"filter": "my"}) + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Show 1 new or updated thread")
