from django.urls import reverse

from ...test import assert_contains
from ..create import create_post_edit


def test_thread_post_edit_restore_view_restores_user_editable_post_on_post_request(
    user_client, user, thread, user_reply
):
    post_edit = create_post_edit(
        post=user_reply,
        user=user,
        old_content="Lorem ipsum",
        new_content=user_reply.original,
    )

    response = user_client.post(
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": user_reply.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
        + f"#post-{user_reply.id}"
    )

    user_reply.refresh_from_db()
    assert user_reply.original == "Lorem ipsum"


def test_thread_post_edit_restore_view_shows_confirmation_page_on_get_request(
    user_client, user, thread, user_reply
):
    post_edit = create_post_edit(
        post=user_reply,
        user=user,
        old_content="Lorem ipsum",
        new_content=user_reply.original,
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": user_reply.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )
    assert_contains(
        response, "Are you sure you want to restore this post to before this edit?"
    )
    assert_contains(
        response,
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": user_reply.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_thread_post_edit_restore_view_shows_login_required_page_to_anonymous_user(
    client, thread, post
):
    response = client.get(
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": 1,
            },
        ),
    )
    assert_contains(response, "Sign in to continue", status_code=401)
