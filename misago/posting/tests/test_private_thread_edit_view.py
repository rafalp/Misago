import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from ...test import (
    assert_contains,
    assert_contains_element,
    assert_not_contains,
    assert_not_contains_element,
)


def test_private_thread_edit_view_displays_login_page_to_guests(
    client, user_private_thread
):
    response = client.get(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Sign in to edit threads")


def test_private_thread_edit_view_displays_error_403_to_users_without_private_threads_permission(
    user_client, members_group, user_private_thread
):
    members_group.can_use_private_threads = False
    members_group.save()

    response = user_client.get(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "You can&#x27;t use private threads.", 403)


def test_private_thread_edit_view_displays_error_404_to_users_who_cant_see_thread(
    user_client, private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": private_thread.id,
                "slug": private_thread.slug,
            },
        )
    )
    assert response.status_code == 404


def test_private_thread_edit_view_displays_error_403_to_users_who_cant_edit_threads(
    user_client, members_group, user_private_thread
):
    members_group.can_edit_own_threads = False
    members_group.save()

    response = user_client.get(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "You can&#x27;t edit threads.", 403)


def test_private_thread_edit_view_displays_error_403_to_users_who_cant_edit_other_users_threads(
    user_client, other_user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "You can&#x27;t edit other users&#x27; threads.", 403)
