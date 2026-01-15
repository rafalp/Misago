from django.urls import reverse

from ...test import assert_contains


def test_private_thread_post_edit_unhide_view_shows_login_required_page_to_anonymous_user(
    client, other_user_private_thread
):
    post = other_user_private_thread.first_post

    response = client.get(
        reverse(
            "misago:private-thread-post-edit-unhide",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "post_edit_id": 1,
            },
        ),
    )
    assert_contains(response, "Sign in to view private threads", status_code=401)
