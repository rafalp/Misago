from django.urls import reverse

from ...test import assert_contains
from ..create import create_post_edit


def test_thread_post_edits_view_shows_empty(user_client, thread, post):
    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
    )
    assert_contains(response, "This post has no edit history.")


def test_thread_post_edits_view_shows_empty_to_anonymous_user(client, thread, post):
    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
    )
    assert_contains(response, "This post has no edit history.")


def test_thread_post_edits_view_shows_empty_in_htmx(user_client, thread, post):
    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "This post has no edit history.")


def test_thread_post_edits_view_shows_empty_to_anonymous_user_in_htmx(
    client, thread, post
):
    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "This post has no edit history.")


def test_thread_post_edits_view_shows_empty_in_modal(user_client, thread, post):
    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "This post has no edit history.")


def test_thread_post_edits_view_shows_empty_to_anonymous_user_in_modal(
    client, thread, post
):
    response = client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "This post has no edit history.")


def test_thread_post_edits_view_redirects_to_first_edit(user_client, thread, post):
    create_post_edit(post=post, user="Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread-post-edits",
        kwargs={
            "thread_id": thread.id,
            "slug": thread.slug,
            "post_id": post.id,
            "page": 1,
        },
    )


def test_thread_post_edits_view_redirects_to_first_edit_in_htmx(
    user_client, thread, post
):
    create_post_edit(post=post, user="Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        ),
        headers={"hx-request": "true"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread-post-edits",
        kwargs={
            "thread_id": thread.id,
            "slug": thread.slug,
            "post_id": post.id,
            "page": 1,
        },
    )


def test_thread_post_edits_view_redirects_to_first_edit_in_modal(
    user_client, thread, post
):
    create_post_edit(post=post, user="Moderator")

    response = user_client.get(
        reverse(
            "misago:thread-post-edits",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread-post-edits",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 1,
            },
        )
        + "?modal=true"
    )
