from django.urls import reverse

from ...test import assert_contains


def test_thread_reply_view_displays_login_page_to_guests(client, thread):
    response = client.get(
        reverse(
            "misago:thread-reply",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )
    assert_contains(response, "Sign in to reply to threads")


def test_thread_reply_view_displays_posting_form(user_client, thread):
    response = user_client.get(
        reverse(
            "misago:thread-reply",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, thread.title)
