from django.urls import reverse

from ...test import assert_contains, assert_not_contains
from ..create import create_post_edit
from ..hide import hide_post_edit


def test_private_thread_post_edit_unhide_view_unhides_hidden_post_edit_on_post(
    thread_reply_factory, moderator_client, user, other_user_private_thread
):
    post = thread_reply_factory(other_user_private_thread, poster=user)

    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )
    hide_post_edit(post_edit, "Moderator")

    response = moderator_client.post(
        reverse(
            "misago:private-thread-post-edit-unhide",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread-post-edits",
        kwargs={
            "thread_id": other_user_private_thread.id,
            "slug": other_user_private_thread.slug,
            "post_id": post.id,
            "page": 1,
        },
    )

    post_edit.refresh_from_db()
    assert not post_edit.is_hidden


def test_private_thread_post_edit_unhide_view_unhides_hidden_post_edit_on_post_in_htmx(
    thread_reply_factory, moderator_client, user, other_user_private_thread
):
    post = thread_reply_factory(other_user_private_thread, poster=user)

    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )
    hide_post_edit(post_edit, "Moderator")

    response = moderator_client.post(
        reverse(
            "misago:private-thread-post-edit-unhide",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "Edit contents hidden")

    post_edit.refresh_from_db()
    assert not post_edit.is_hidden


def test_private_thread_post_edit_unhide_view_unhides_hidden_post_edit_on_post_in_modal(
    thread_reply_factory, moderator_client, user, other_user_private_thread
):
    post = thread_reply_factory(other_user_private_thread, poster=user)

    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )
    hide_post_edit(post_edit, "Moderator")

    response = moderator_client.post(
        reverse(
            "misago:private-thread-post-edit-unhide",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "Edit contents hidden")

    post_edit.refresh_from_db()
    assert not post_edit.is_hidden


def test_private_thread_post_edit_unhide_view_does_nothing_for_visible_post_edit_on_post(
    thread_reply_factory, moderator_client, user, other_user_private_thread
):
    post = thread_reply_factory(other_user_private_thread, poster=user)

    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )

    response = moderator_client.post(
        reverse(
            "misago:private-thread-post-edit-unhide",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread-post-edits",
        kwargs={
            "thread_id": other_user_private_thread.id,
            "slug": other_user_private_thread.slug,
            "post_id": post.id,
            "page": 1,
        },
    )

    post_edit.refresh_from_db()
    assert not post_edit.is_hidden


def test_private_thread_post_edit_unhide_view_does_nothing_for_visible_post_edit_on_post_in_htmx(
    thread_reply_factory, moderator_client, user, other_user_private_thread
):
    post = thread_reply_factory(other_user_private_thread, poster=user)

    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )

    response = moderator_client.post(
        reverse(
            "misago:private-thread-post-edit-unhide",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "Edit contents hidden")

    post_edit.refresh_from_db()
    assert not post_edit.is_hidden


def test_private_thread_post_edit_unhide_view_does_nothing_for_visible_post_edit_on_post_in_modal(
    thread_reply_factory, moderator_client, user, other_user_private_thread
):
    post = thread_reply_factory(other_user_private_thread, poster=user)

    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )

    response = moderator_client.post(
        reverse(
            "misago:private-thread-post-edit-unhide",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "Edit contents hidden")

    post_edit.refresh_from_db()
    assert not post_edit.is_hidden


def test_private_thread_post_edit_unhide_view_shows_method_not_allowed_error_on_get_request(
    thread_reply_factory, moderator_client, user, other_user_private_thread
):
    post = thread_reply_factory(other_user_private_thread, poster=user)

    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )
    hide_post_edit(post_edit, "Moderator")

    response = moderator_client.get(
        reverse(
            "misago:private-thread-post-edit-unhide",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )
    assert response.status_code == 405


def test_private_thread_post_edit_unhide_view_shows_error_403_if_post_edit_cant_be_unhidden(
    thread_reply_factory, user_client, user, other_user_private_thread
):
    post = thread_reply_factory(other_user_private_thread, poster=user)

    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )
    hide_post_edit(post_edit, "Moderator")

    response = user_client.post(
        reverse(
            "misago:private-thread-post-edit-unhide",
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
        "You can’t unhide hidden post edits.",
        status_code=403,
    )


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


def test_private_thread_post_edit_unhide_view_returns_error_403_if_user_has_no_private_threads_permission(
    user_client, members_group, other_user_private_thread
):
    members_group.can_use_private_threads = False
    members_group.save()

    post = other_user_private_thread.first_post

    response = user_client.post(
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
    assert_contains(response, "You can&#x27;t use private threads.", status_code=403)


def test_private_thread_post_edit_unhide_view_returns_error_404_if_thread_doesnt_exist(
    user_client,
):
    response = user_client.post(
        reverse(
            "misago:private-thread-post-edit-unhide",
            kwargs={
                "thread_id": 1,
                "slug": "doesnt-exist",
                "post_id": 1,
                "post_edit_id": 1,
            },
        ),
    )
    assert response.status_code == 404


def test_private_thread_post_edit_unhide_view_returns_error_404_if_user_cant_see_thread(
    thread_reply_factory, user_client, user, private_thread
):
    post = thread_reply_factory(private_thread, poster=user)
    post_edit = create_post_edit(post=post, user=user)

    response = user_client.post(
        reverse(
            "misago:private-thread-post-edit-unhide",
            kwargs={
                "thread_id": private_thread.id,
                "slug": private_thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )
    assert response.status_code == 404


def test_private_thread_post_edit_unhide_view_returns_error_404_if_thread_post_doesnt_exist(
    user_client, other_user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-post-edit-unhide",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": 1,
                "post_edit_id": 1,
            },
        ),
    )
    assert response.status_code == 404


def test_private_thread_post_edit_unhide_view_returns_error_404_if_thread_post_doesnt_exist(
    user_client, other_user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-post-edit-unhide",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": 1,
                "post_edit_id": 1,
            },
        ),
    )
    assert response.status_code == 404


def test_private_thread_post_edit_unhide_view_returns_error_404_if_thread_post_belongs_to_other_thread(
    user_client, other_user_private_thread, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-post-edit-unhide",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": user_private_thread.first_post_id,
                "post_edit_id": 1,
            },
        ),
    )
    assert response.status_code == 404
