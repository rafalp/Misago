import pytest
from django.urls import reverse

from ...permissions.enums import CanHideOwnPostEdits
from ...test import assert_contains
from ..create import create_post_edit
from ..models import PostEdit


def test_thread_post_edit_delete_view_deletes_only_post_edit_on_post(
    thread_reply_factory, user_client, members_group, user, thread
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    post = thread_reply_factory(thread, poster=user)

    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )

    response = user_client.post(
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
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

    with pytest.raises(PostEdit.DoesNotExist):
        post_edit.refresh_from_db()


def test_thread_post_edit_delete_view_deletes_only_post_edit_on_post_in_htmx(
    thread_reply_factory, user_client, members_group, user, thread
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    post = thread_reply_factory(thread, poster=user)

    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )

    response = user_client.post(
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "This post has no edit history.")

    with pytest.raises(PostEdit.DoesNotExist):
        post_edit.refresh_from_db()


def test_thread_post_edit_delete_view_deletes_only_post_edit_on_post_in_modal(
    thread_reply_factory, user_client, members_group, user, thread
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    post = thread_reply_factory(thread, poster=user)

    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )

    response = user_client.post(
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "This post has no edit history.")

    with pytest.raises(PostEdit.DoesNotExist):
        post_edit.refresh_from_db()


def test_thread_post_edit_delete_view_shows_confirmation_page_on_get_request(
    thread_reply_factory, user_client, members_group, user, thread
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    post = thread_reply_factory(thread, poster=user)

    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Are you sure you want to delete this post edit?")


def test_thread_post_edit_delete_view_shows_login_required_page_to_anonymous_user(
    client, thread, post
):
    response = client.get(
        reverse(
            "misago:thread-post-edit-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": 1,
            },
        ),
    )
    assert_contains(response, "Sign in to continue", status_code=401)
