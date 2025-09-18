from django.urls import reverse

from ...test import assert_contains


def test_private_thread_replies_view_shows_thread_members(
    user_client, user_private_thread, user, other_user, moderator
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, user_private_thread.title)
    assert_contains(response, "3 members")
    assert_contains(response, user.username)
    assert_contains(response, other_user.username)
    assert_contains(response, moderator.username)
