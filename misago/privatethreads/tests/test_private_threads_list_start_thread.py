from django.urls import reverse

from ...test import assert_contains, assert_not_contains


def test_private_threads_list_displays_start_thread_button_to_user_with_permission(
    user_client,
):
    response = user_client.get(reverse("misago:private-thread-list"))
    assert_contains(response, reverse("misago:private-thread-start"))


def test_private_threads_list_hides_start_thread_button_from_user_without_permission(
    user, user_client
):
    user.group.can_start_private_threads = False
    user.group.save()

    response = user_client.get(reverse("misago:private-thread-list"))
    assert_not_contains(response, reverse("misago:private-thread-start"))
