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
