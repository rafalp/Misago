from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...test import assert_contains, assert_not_contains
from ...threads.enums import ThreadsListsPolling
from ..models import PrivateThreadMember


def test_private_thread_list_view_includes_polling_if_its_not_empty(
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
def test_private_thread_list_view_excludes_polling_if_its_disabled(
    thread_factory, user, user_client, private_threads_category
):
    thread = thread_factory(private_threads_category)
    PrivateThreadMember.objects.create(thread=thread, user=user)
    response = user_client.get(private_threads_category.get_absolute_url())
    assert_not_contains(
        response, private_threads_category.get_absolute_url() + "?poll_new="
    )


def test_private_thread_list_view_poll_returns_update_button_for_hx_request_if_there_are_new_threads(
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


def test_private_thread_list_view_poll_returns_update_button_for_hx_request_if_there_are_new_threads_after_thread(
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


def test_private_thread_list_view_poll_doesnt_return_update_button_for_hx_request_if_there_are_no_new_threads(
    user_client, private_threads_category
):
    response = user_client.get(
        private_threads_category.get_absolute_url() + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "new or updated thread")


def test_private_thread_list_view_poll_doesnt_return_update_button_for_hx_request_if_there_are_no_new_threads_after_thread(
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
def test_private_thread_list_view_poll_doesnt_return_update_button_if_polling_is_disabled(
    thread_factory, user, user_client, private_threads_category
):
    thread = thread_factory(private_threads_category)
    PrivateThreadMember.objects.create(thread=thread, user=user)

    response = user_client.get(
        private_threads_category.get_absolute_url() + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "new or updated thread")


def test_private_thread_list_view_poll_doesnt_return_button_if_request_is_not_htmx(
    thread_factory, user, user_client, private_threads_category
):
    thread = thread_factory(private_threads_category)
    PrivateThreadMember.objects.create(thread=thread, user=user)

    response = user_client.get(
        private_threads_category.get_absolute_url() + "?poll_new=0"
    )
    assert_not_contains(response, "new or updated thread")


def test_private_thread_list_view_poll_shows_error_to_users_without_permission(
    user_client, private_threads_category, members_group
):
    members_group.can_use_private_threads = False
    members_group.save()

    response = user_client.get(
        private_threads_category.get_absolute_url() + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "You can't use private threads.", status_code=403)


def test_private_thread_list_view_poll_doesnt_return_button_if_new_threads_are_not_visible(
    thread_factory, user_client, private_threads_category, other_user
):
    thread = thread_factory(private_threads_category)
    PrivateThreadMember.objects.create(thread=thread, user=other_user)

    response = user_client.get(
        private_threads_category.get_absolute_url() + "?poll_new=0",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "new or updated thread")


def test_private_thread_list_view_poll_raises_404_error_if_filter_is_invalid(
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


def test_private_thread_list_view_poll_filters_threads(
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
