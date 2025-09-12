import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from ...test import (
    assert_contains,
    assert_contains_element,
    assert_not_contains,
    assert_not_contains_element,
)


def test_private_thread_post_edit_view_displays_login_page_to_guests(
    thread_reply_factory, client, other_user_private_thread
):
    post = thread_reply_factory(other_user_private_thread)

    response = client.get(
        reverse(
            "misago:private-thread-post-edit",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert_contains(response, "Sign in to edit posts")
