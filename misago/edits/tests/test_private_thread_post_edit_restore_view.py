from django.urls import reverse

from ...test import assert_contains
from ..create import create_post_edit


def test_private_thread_post_edit_restore_view_restores_user_editable_post_on_post_request(
    thread_reply_factory, user_client, user, other_user_private_thread
):
    post = thread_reply_factory(other_user_private_thread, poster=user)

    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-post-edit-restore",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
        + f"#post-{post.id}"
    )

    post.refresh_from_db()
    assert post.original == "Lorem ipsum"


def test_private_thread_post_edit_restore_view_shows_confirmation_page_on_get_request(
    thread_reply_factory, user_client, user, other_user_private_thread
):
    post = thread_reply_factory(other_user_private_thread, poster=user)

    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edit-restore",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
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
            "misago:private-thread-post-edit-restore",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )


def test_private_thread_post_edit_restore_view_shows_error_403_if_post_edit_cant_be_restored(
    thread_reply_factory, user_client, user, other_user_private_thread
):
    post = thread_reply_factory(other_user_private_thread, poster=user)

    post_edit = create_post_edit(post=post, user=user)

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edit-restore",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )
    assert_contains(
        response,
        "You can’t restore the post from this edit.",
        status_code=403,
    )


def test_private_thread_post_edit_restore_view_shows_error_403_if_post_is_not_editable(
    thread_reply_factory, user_client, user, members_group, other_user_private_thread
):
    members_group.can_edit_own_posts = False
    members_group.save()

    post = thread_reply_factory(other_user_private_thread, poster=user)

    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content="Dolor met",
    )

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edit-restore",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )
    assert_contains(response, "You can&#x27;t edit posts.", status_code=403)


def test_private_thread_post_edit_restore_view_shows_login_required_page_to_anonymous_user(
    client, other_user_private_thread
):
    post = other_user_private_thread.first_post

    response = client.get(
        reverse(
            "misago:private-thread-post-edit-restore",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "post_edit_id": 1,
            },
        ),
    )
    assert_contains(response, "Sign in to view private threads", status_code=401)


def test_private_thread_post_edit_restore_view_returns_error_403_if_user_has_no_private_threads_permission(
    user_client, members_group, other_user_private_thread
):
    members_group.can_use_private_threads = False
    members_group.save()

    post = other_user_private_thread.first_post

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edit-restore",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "post_edit_id": 1,
            },
        ),
    )
    assert_contains(response, "You can&#x27;t use private threads.", status_code=403)


def test_private_thread_post_edit_restore_view_returns_error_404_if_thread_doesnt_exist(
    user_client,
):
    response = user_client.get(
        reverse(
            "misago:private-thread-post-edit-restore",
            kwargs={
                "thread_id": 1,
                "slug": "doesnt-exist",
                "post_id": 1,
                "post_edit_id": 1,
            },
        ),
    )
    assert response.status_code == 404


def test_private_thread_post_edit_restore_view_returns_error_404_if_user_cant_see_thread(
    thread_reply_factory, user_client, user, private_thread
):
    post = thread_reply_factory(private_thread, poster=user)
    post_edit = create_post_edit(post=post, user=user)

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edit-restore",
            kwargs={
                "thread_id": private_thread.id,
                "slug": private_thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )
    assert response.status_code == 404
