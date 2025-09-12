import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from ...test import (
    assert_contains,
    assert_contains_element,
    assert_not_contains,
    assert_not_contains_element,
)


def test_private_thread_post_edit_view_displays_login_page_to_guests(
    thread_reply_factory, client, other_user_private_thread
):
    post = thread_reply_factory(other_user_private_thread)

    response = client.get(
        reverse(
            "misago:private-thread-post-edit",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert_contains(response, "Sign in to edit posts")


def test_private_thread_post_edit_view_displays_error_403_to_users_without_private_threads_permission(
    thread_reply_factory, user_client, members_group, user_private_thread
):
    post = thread_reply_factory(user_private_thread)

    members_group.can_use_private_threads = False
    members_group.save()

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert_contains(response, "You can&#x27;t use private threads.", 403)


def test_private_thread_post_edit_view_displays_error_404_to_users_who_cant_see_thread(
    thread_reply_factory, user_client, private_thread
):
    post = thread_reply_factory(private_thread)

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edit",
            kwargs={
                "thread_id": private_thread.id,
                "slug": private_thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert response.status_code == 404


def test_private_thread_post_edit_view_displays_error_403_to_users_who_cant_edit_posts(
    thread_reply_factory, user_client, user, members_group, other_user_private_thread
):
    post = thread_reply_factory(other_user_private_thread, poster=user)

    members_group.can_edit_own_posts = False
    members_group.save()

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edit",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert_contains(response, "You can&#x27;t edit posts.", 403)


def test_private_thread_post_edit_view_displays_error_403_to_users_who_cant_edit_other_users_posts(
    thread_reply_factory,
    user_client,
    other_user,
    other_user_private_thread,
):
    post = thread_reply_factory(other_user_private_thread, poster=other_user)

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edit",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert_contains(response, "You can&#x27;t edit other users&#x27; posts.", 403)


def test_private_thread_post_edit_view_displays_error_403_to_users_who_cant_edit_deleted_users_posts(
    thread_reply_factory,
    user_client,
    other_user_private_thread,
):
    post = thread_reply_factory(other_user_private_thread)

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edit",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert_contains(response, "You can&#x27;t edit other users&#x27; posts.", 403)


def test_private_thread_post_edit_view_displays_error_403_to_users_who_cant_see_post_contents(
    thread_reply_factory, user_client, user, other_user_private_thread
):
    post = thread_reply_factory(other_user_private_thread, poster=user, is_hidden=True)

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edit",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert_contains(response, "You can&#x27;t edit hidden posts.", 403)


def test_private_thread_post_edit_view_displays_edit_form(
    thread_reply_factory, user_client, user, other_user_private_thread
):
    post = thread_reply_factory(other_user_private_thread, poster=user)

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edit",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert_contains(response, "Edit post")
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, post.original)


def test_private_thread_post_edit_view_displays_edit_form_for_moderator(
    thread_reply_factory, moderator_client, user, other_user_private_thread
):
    post = thread_reply_factory(other_user_private_thread, poster=user)

    response = moderator_client.get(
        reverse(
            "misago:private-thread-post-edit",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert_contains(response, "Edit post")
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, post.original)


def test_private_thread_post_edit_view_displays_inline_edit_form_in_htmx(
    thread_reply_factory, user_client, user, other_user_private_thread
):
    post = thread_reply_factory(other_user_private_thread, poster=user)

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edit",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        )
        + "?inline=true",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Save")
    assert_contains(response, post.original)
    assert_contains(response, "?inline=true")
