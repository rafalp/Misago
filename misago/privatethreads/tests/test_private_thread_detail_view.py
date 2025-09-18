from django.urls import reverse

from ...test import assert_contains


def test_private_thread_detail_view_displays_login_page_to_guests(db, client):
    response = client.get(
        reverse(
            "misago:private-thread", kwargs={"thread_id": 1, "slug": "private-thread"}
        )
    )
    assert_contains(response, "Sign in to view private threads")
