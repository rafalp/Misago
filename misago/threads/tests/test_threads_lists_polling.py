from django.urls import reverse

from ...categories.models import Category
from ...conf.test import override_dynamic_settings
from ...privatethreads.models import PrivateThreadMember
from ...test import assert_contains, assert_not_contains
from ..enums import ThreadsListsPolling


@override_dynamic_settings(index_view="categories")
def test_threads_list_includes_polling_if_its_not_empty(
    thread_factory, client, default_category
):
    thread = thread_factory(default_category)

    response = client.get(reverse("misago:threads"))
    assert_contains(
        response, reverse("misago:threads") + f"?poll_new={thread.last_post_id}"
    )


@override_dynamic_settings(
    index_view="categories", threads_lists_polling=ThreadsListsPolling.DISABLED
)
def test_threads_list_excludes_polling_for_guests_if_its_disabled(
    thread_factory, client, default_category
):
    thread_factory(default_category)

    response = client.get(reverse("misago:threads"))
    assert_not_contains(response, reverse("misago:threads") + "?poll_new=")


@override_dynamic_settings(
    index_view="categories", threads_lists_polling=ThreadsListsPolling.DISABLED
)
def test_threads_list_excludes_polling_for_authenticated_if_its_disabled(
    thread_factory, user_client, default_category
):
    thread_factory(default_category)

    response = user_client.get(reverse("misago:threads"))
    assert_not_contains(response, reverse("misago:threads") + "?poll_new=")


@override_dynamic_settings(
    index_view="categories", threads_lists_polling=ThreadsListsPolling.ENABLED_FOR_USERS
)
def test_threads_list_excludes_polling_for_guest_if_its_enabled_for_users(
    thread_factory, client, default_category
):
    thread_factory(default_category)

    response = client.get(reverse("misago:threads"))
    assert_not_contains(response, reverse("misago:threads") + "?poll_new=")


@override_dynamic_settings(
    index_view="categories", threads_lists_polling=ThreadsListsPolling.ENABLED_FOR_USERS
)
def test_threads_list_includes_polling_for_user_if_its_enabled_for_users(
    thread_factory, user_client, default_category
):
    thread = thread_factory(default_category)

    response = user_client.get(reverse("misago:threads"))
    assert_contains(
        response, reverse("misago:threads") + f"?poll_new={thread.last_post_id}"
    )


@override_dynamic_settings(index_view="categories")
def test_threads_list_poll_returns_update_button_for_hx_request_if_there_are_new_threads(
    thread_factory, client, default_category
):
    thread_factory(default_category)
    thread_factory(default_category)

    response = client.get(
        reverse("misago:threads") + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Show 2 new or updated threads")


@override_dynamic_settings(index_view="categories")
def test_threads_list_poll_returns_update_button_for_hx_request_if_there_are_new_threads_after_thread(
    thread_factory, client, default_category
):
    thread = thread_factory(default_category)
    thread_factory(default_category)
    thread_factory(default_category)

    response = client.get(
        reverse("misago:threads") + f"?poll_new={thread.last_post_id}",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Show 2 new or updated threads")


@override_dynamic_settings(index_view="categories")
def test_threads_list_poll_doesnt_return_update_button_for_hx_request_if_there_are_no_new_threads(
    db, client
):
    response = client.get(
        reverse("misago:threads") + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "new or updated thread")


@override_dynamic_settings(index_view="categories")
def test_threads_list_poll_doesnt_return_update_button_for_hx_request_if_there_are_no_new_threads_after_thread(
    thread_factory, client, default_category
):
    thread = thread_factory(default_category)
    response = client.get(
        reverse("misago:threads") + f"?poll_new={thread.last_post_id}",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "new or updated thread")


@override_dynamic_settings(
    index_view="categories", threads_lists_polling=ThreadsListsPolling.DISABLED
)
def test_threads_list_poll_doesnt_return_update_button_for_guest_hx_request_if_polling_is_disabled(
    thread_factory, client, default_category
):
    thread_factory(default_category)
    thread_factory(default_category)

    response = client.get(
        reverse("misago:threads") + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "new or updated thread")


@override_dynamic_settings(
    index_view="categories", threads_lists_polling=ThreadsListsPolling.DISABLED
)
def test_threads_list_poll_doesnt_return_update_button_for_user_hx_request_if_polling_is_disabled(
    thread_factory, client, default_category
):
    thread_factory(default_category)
    thread_factory(default_category)

    response = client.get(
        reverse("misago:threads") + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "new or updated thread")


@override_dynamic_settings(
    index_view="categories", threads_lists_polling=ThreadsListsPolling.ENABLED_FOR_USERS
)
def test_threads_list_poll_doesnt_return_update_button_for_guest_hx_request_if_polling_is_disabled_for_anonymous(
    thread_factory, client, default_category
):
    thread_factory(default_category)
    thread_factory(default_category)

    response = client.get(
        reverse("misago:threads") + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "new or updated thread")


@override_dynamic_settings(
    index_view="categories", threads_lists_polling=ThreadsListsPolling.ENABLED_FOR_USERS
)
def test_threads_list_poll_returns_update_button_for_user_hx_request_if_polling_is_disabled_for_anonymous(
    thread_factory, user_client, default_category
):
    thread_factory(default_category)
    thread_factory(default_category)

    response = user_client.get(
        reverse("misago:threads") + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Show 2 new or updated threads")


@override_dynamic_settings(index_view="categories")
def test_threads_list_poll_doesnt_return_button_if_request_is_not_htmx(
    thread_factory, client, default_category
):
    thread_factory(default_category)
    thread_factory(default_category)

    response = client.get(reverse("misago:threads") + "?poll_new=0")
    assert_not_contains(response, "Show 2 new or updated threads")


@override_dynamic_settings(index_view="categories")
def test_threads_list_poll_uses_category_permissions(
    thread_factory, client, default_category, hidden_category
):
    thread_factory(hidden_category)
    thread_factory(default_category)

    response = client.get(
        reverse("misago:threads") + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Show 1 new or updated thread")


@override_dynamic_settings(index_view="categories")
def test_threads_list_poll_raises_404_error_if_filter_is_invalid(
    thread_factory, default_category, user, user_client
):
    thread_factory(default_category, starter=user)
    response = user_client.get(
        reverse("misago:threads", kwargs={"filter": "invalid"}) + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


@override_dynamic_settings(index_view="categories")
def test_threads_list_poll_filters_threads(
    thread_factory, default_category, user, user_client
):
    thread_factory(default_category, starter=user)
    thread_factory(default_category)

    response = user_client.get(
        reverse("misago:threads", kwargs={"filter": "my"}) + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Show 1 new or updated thread")


def test_category_threads_list_includes_polling_if_its_not_empty(
    thread_factory, client, default_category
):
    thread = thread_factory(default_category)

    response = client.get(default_category.get_absolute_url())
    assert_contains(
        response,
        default_category.get_absolute_url() + f"?poll_new={thread.last_post_id}",
    )


@override_dynamic_settings(threads_lists_polling=ThreadsListsPolling.DISABLED)
def test_category_threads_list_excludes_polling_for_guests_if_its_disabled(
    thread_factory, client, default_category
):
    thread_factory(default_category)

    response = client.get(default_category.get_absolute_url())
    assert_not_contains(response, default_category.get_absolute_url() + "?poll_new=")


@override_dynamic_settings(threads_lists_polling=ThreadsListsPolling.DISABLED)
def test_category_threads_list_excludes_polling_for_authenticated_if_its_disabled(
    thread_factory, user_client, default_category
):
    thread_factory(default_category)

    response = user_client.get(default_category.get_absolute_url())
    assert_not_contains(response, default_category.get_absolute_url() + "?poll_new=")


@override_dynamic_settings(threads_lists_polling=ThreadsListsPolling.ENABLED_FOR_USERS)
def test_category_threads_list_excludes_polling_for_guest_if_its_enabled_for_users(
    thread_factory, client, default_category
):
    thread_factory(default_category)

    response = client.get(default_category.get_absolute_url())
    assert_not_contains(response, default_category.get_absolute_url() + "?poll_new=")


@override_dynamic_settings(threads_lists_polling=ThreadsListsPolling.ENABLED_FOR_USERS)
def test_category_threads_list_includes_polling_for_user_if_its_enabled_for_users(
    thread_factory, user_client, default_category
):
    thread = thread_factory(default_category)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(
        response,
        default_category.get_absolute_url() + f"?poll_new={thread.last_post_id}",
    )


def test_category_threads_list_poll_returns_update_button_for_hx_request_if_there_are_new_threads(
    thread_factory, client, default_category
):
    thread_factory(default_category)
    thread_factory(default_category)

    response = client.get(
        default_category.get_absolute_url() + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Show 2 new or updated threads")


def test_category_threads_list_poll_returns_update_button_for_hx_request_if_there_are_new_threads_after_thread(
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


def test_category_threads_list_poll_doesnt_return_update_button_for_hx_request_if_there_are_no_new_threads(
    client, default_category
):
    response = client.get(
        default_category.get_absolute_url() + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "new or updated thread")


def test_category_threads_list_poll_doesnt_return_update_button_for_hx_request_if_there_are_no_new_threads_after_thread(
    thread_factory, client, default_category
):
    thread = thread_factory(default_category)
    response = client.get(
        default_category.get_absolute_url() + f"?poll_new={thread.last_post_id}",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "new or updated thread")


@override_dynamic_settings(threads_lists_polling=ThreadsListsPolling.DISABLED)
def test_category_threads_list_poll_doesnt_return_update_button_for_guest_hx_request_if_polling_is_disabled(
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
def test_category_threads_list_poll_doesnt_return_update_button_for_user_hx_request_if_polling_is_disabled(
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
def test_category_threads_list_poll_doesnt_return_update_button_for_guest_hx_request_if_polling_is_disabled_for_anonymous(
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
def test_category_threads_list_poll_returns_update_button_for_user_hx_request_if_polling_is_disabled_for_anonymous(
    thread_factory, user_client, default_category
):
    thread_factory(default_category)
    thread_factory(default_category)

    response = user_client.get(
        default_category.get_absolute_url() + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Show 2 new or updated threads")


def test_category_threads_list_poll_doesnt_return_button_if_request_is_not_htmx(
    thread_factory, client, default_category
):
    thread_factory(default_category)
    thread_factory(default_category)

    response = client.get(default_category.get_absolute_url() + "?poll_new=0")
    assert_not_contains(response, "Show 2 new or updated threads")


def test_category_threads_list_poll_uses_category_permissions(
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


def test_category_threads_list_poll_raises_404_error_if_filter_is_invalid(
    thread_factory, default_category, user, user_client
):
    thread_factory(default_category, starter=user)
    response = user_client.get(
        reverse(
            "misago:category",
            kwargs={
                "id": default_category.id,
                "slug": default_category.slug,
                "filter": "invalid",
            },
        )
        + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


def test_category_threads_list_poll_filters_threads(
    thread_factory, default_category, user, user_client
):
    thread_factory(default_category, starter=user)
    thread_factory(default_category)

    response = user_client.get(
        reverse(
            "misago:category",
            kwargs={
                "id": default_category.id,
                "slug": default_category.slug,
                "filter": "my",
            },
        )
        + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Show 1 new or updated thread")


def test_private_threads_list_includes_polling_if_its_not_empty(
    thread_factory, user, user_client, private_threads_category
):
    thread = thread_factory(private_threads_category)
    PrivateThreadMember.objects.create(thread=thread, user=user)

    response = user_client.get(private_threads_category.get_absolute_url())
    assert_contains(
        response,
        private_threads_category.get_absolute_url()
        + f"?poll_new={thread.last_post_id}",
    )


@override_dynamic_settings(threads_lists_polling=ThreadsListsPolling.DISABLED)
def test_private_threads_list_excludes_polling_if_its_disabled(
    thread_factory, user, user_client, private_threads_category
):
    thread = thread_factory(private_threads_category)
    PrivateThreadMember.objects.create(thread=thread, user=user)

    response = user_client.get(private_threads_category.get_absolute_url())
    assert_not_contains(
        response, private_threads_category.get_absolute_url() + "?poll_new="
    )


def test_private_threads_list_poll_returns_update_button_for_hx_request_if_there_are_new_threads(
    thread_factory, user, user_client, private_threads_category
):
    thread_1 = thread_factory(private_threads_category)
    PrivateThreadMember.objects.create(thread=thread_1, user=user)

    thread_2 = thread_factory(private_threads_category)
    PrivateThreadMember.objects.create(thread=thread_2, user=user)

    response = user_client.get(
        private_threads_category.get_absolute_url() + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Show 2 new or updated threads")


def test_private_threads_list_poll_returns_update_button_for_hx_request_if_there_are_new_threads_after_thread(
    thread_factory, user, user_client, private_threads_category
):
    threads = [
        thread_factory(private_threads_category),
        thread_factory(private_threads_category),
        thread_factory(private_threads_category),
    ]

    for thread in threads:
        PrivateThreadMember.objects.create(thread=thread, user=user)

    response = user_client.get(
        private_threads_category.get_absolute_url()
        + f"?poll_new={threads[0].last_post_id}",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Show 2 new or updated threads")


def test_private_threads_list_poll_doesnt_return_update_button_for_hx_request_if_there_are_no_new_threads(
    user_client, private_threads_category
):
    response = user_client.get(
        private_threads_category.get_absolute_url() + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "new or updated thread")


def test_private_threads_list_poll_doesnt_return_update_button_for_hx_request_if_there_are_no_new_threads_after_thread(
    thread_factory, user, user_client, private_threads_category
):
    thread = thread_factory(private_threads_category)
    PrivateThreadMember.objects.create(thread=thread, user=user)

    response = user_client.get(
        private_threads_category.get_absolute_url()
        + f"?poll_new={thread.last_post_id}",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "new or updated thread")


@override_dynamic_settings(threads_lists_polling=ThreadsListsPolling.DISABLED)
def test_private_threads_list_poll_doesnt_return_update_button_if_polling_is_disabled(
    thread_factory, user, user_client, private_threads_category
):
    thread = thread_factory(private_threads_category)
    PrivateThreadMember.objects.create(thread=thread, user=user)

    response = user_client.get(
        private_threads_category.get_absolute_url() + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "new or updated thread")


def test_private_threads_list_poll_doesnt_return_button_if_request_is_not_htmx(
    thread_factory, user, user_client, private_threads_category
):
    thread = thread_factory(private_threads_category)
    PrivateThreadMember.objects.create(thread=thread, user=user)

    response = user_client.get(
        private_threads_category.get_absolute_url() + "?poll_new=0"
    )
    assert_not_contains(response, "new or updated thread")


def test_private_threads_list_poll_shows_error_to_users_without_permission(
    user_client, private_threads_category, members_group
):
    members_group.can_use_private_threads = False
    members_group.save()

    response = user_client.get(
        private_threads_category.get_absolute_url() + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "You can't use private threads.", status_code=403)


def test_private_threads_list_poll_doesnt_return_button_if_new_threads_are_not_visible(
    thread_factory, user_client, private_threads_category, other_user
):
    thread = thread_factory(private_threads_category)
    PrivateThreadMember.objects.create(thread=thread, user=other_user)

    response = user_client.get(
        private_threads_category.get_absolute_url() + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "new or updated thread")


def test_private_threads_list_poll_raises_404_error_if_filter_is_invalid(
    thread_factory, private_threads_category, user, user_client
):
    thread = thread_factory(private_threads_category, starter=user)
    PrivateThreadMember.objects.create(thread=thread, user=user)

    response = user_client.get(
        reverse("misago:private-thread-list", kwargs={"filter": "invalid"})
        + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


def test_private_threads_list_poll_filters_threads(
    thread_factory, private_threads_category, user, user_client
):
    visible_thread = thread_factory(private_threads_category, starter=user)
    hidden_thread = thread_factory(private_threads_category)

    PrivateThreadMember.objects.create(thread=visible_thread, user=user)
    PrivateThreadMember.objects.create(thread=hidden_thread, user=user)

    response = user_client.get(
        reverse("misago:private-thread-list", kwargs={"filter": "my"}) + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Show 1 new or updated thread")
