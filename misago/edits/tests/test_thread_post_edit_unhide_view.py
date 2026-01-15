from django.urls import reverse

from ...test import assert_contains


def test_thread_post_edit_unhide_view_shows_login_required_page_to_anonymous_user(
    client, thread, post
):
    response = client.get(
        reverse(
            "misago:thread-post-edit-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": 1,
            },
        ),
    )
    assert_contains(response, "Sign in to continue", status_code=401)
