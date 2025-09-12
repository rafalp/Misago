from django.urls import reverse

from ...test import assert_contains


def test_thread_reply_view_displays_login_page_to_guests(client, user_private_thread):
    response = client.get(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Sign in to reply to threads")


def test_private_thread_reply_view_displays_posting_form(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, user_private_thread.title)
