from django.urls import reverse

from ...test import assert_contains


def test_private_thread_post_edits_view_shows_empty(
    user_client, other_user_private_thread
):
    post = other_user_private_thread.first_post

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert_contains(response, "This post has no edit history.")


def test_private_thread_post_edits_view_shows_empty_in_htmx(
    user_client, other_user_private_thread
):
    post = other_user_private_thread.first_post

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "This post has no edit history.")


def test_private_thread_post_edits_view_shows_empty_in_modal(
    user_client, other_user_private_thread
):
    post = other_user_private_thread.first_post

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "This post has no edit history.")
