import pytest
from django.urls import reverse

from ...permissions.enums import CanHideOwnPostEdits
from ...test import assert_contains, assert_not_contains
from ..create import create_post_edit
from ..models import PostEdit


def test_private_thread_post_edit_delete_view_deletes_only_post_edit_on_post(
    thread_reply_factory, user_client, members_group, user, other_user_private_thread
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    post = thread_reply_factory(other_user_private_thread, poster=user)

    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-post-edit-delete",
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

    with pytest.raises(PostEdit.DoesNotExist):
        post_edit.refresh_from_db()


def test_private_thread_post_edit_delete_view_deletes_only_post_edit_on_post_in_htmx(
    thread_reply_factory, user_client, members_group, user, other_user_private_thread
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    post = thread_reply_factory(other_user_private_thread, poster=user)

    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-post-edit-delete",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "This post has no edit history.")

    with pytest.raises(PostEdit.DoesNotExist):
        post_edit.refresh_from_db()


def test_private_thread_post_edit_delete_view_deletes_only_post_edit_on_post_in_modal(
    thread_reply_factory, user_client, members_group, user, other_user_private_thread
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    post = thread_reply_factory(other_user_private_thread, poster=user)

    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-post-edit-delete",
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
    assert_contains(response, "This post has no edit history.")

    with pytest.raises(PostEdit.DoesNotExist):
        post_edit.refresh_from_db()


def test_private_thread_post_edit_delete_view_deletes_first_post_edit_on_post(
    thread_reply_factory, user_client, members_group, user, other_user_private_thread
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    post = thread_reply_factory(other_user_private_thread, poster=user)

    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )
    create_post_edit(
        post=post,
        user=user,
        old_content="Other post edit",
        new_content=post.original,
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-post-edit-delete",
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

    with pytest.raises(PostEdit.DoesNotExist):
        post_edit.refresh_from_db()


def test_private_thread_post_edit_delete_view_deletes_first_post_edit_on_post_in_htmx(
    thread_reply_factory, user_client, members_group, user, other_user_private_thread
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    post = thread_reply_factory(other_user_private_thread, poster=user)

    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )
    other_post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Other post edit",
        new_content=post.original,
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-post-edit-delete",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, other_post_edit.old_content)

    with pytest.raises(PostEdit.DoesNotExist):
        post_edit.refresh_from_db()


def test_private_thread_post_edit_delete_view_deletes_first_post_edit_on_post_in_modal(
    thread_reply_factory, user_client, members_group, user, other_user_private_thread
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    post = thread_reply_factory(other_user_private_thread, poster=user)

    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )
    other_post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Other post edit",
        new_content=post.original,
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-post-edit-delete",
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
    assert_contains(response, other_post_edit.old_content)

    with pytest.raises(PostEdit.DoesNotExist):
        post_edit.refresh_from_db()


def test_private_thread_post_edit_delete_view_deletes_last_post_edit_on_post(
    thread_reply_factory, user_client, members_group, user, other_user_private_thread
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    post = thread_reply_factory(other_user_private_thread, poster=user)

    create_post_edit(
        post=post,
        user=user,
        old_content="Other post edit",
        new_content=post.original,
    )
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-post-edit-delete",
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

    with pytest.raises(PostEdit.DoesNotExist):
        post_edit.refresh_from_db()


def test_private_thread_post_edit_delete_view_deletes_last_post_edit_on_post_in_htmx(
    thread_reply_factory, user_client, members_group, user, other_user_private_thread
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    post = thread_reply_factory(other_user_private_thread, poster=user)

    other_post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Other post edit",
        new_content=post.original,
    )
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-post-edit-delete",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, other_post_edit.old_content)

    with pytest.raises(PostEdit.DoesNotExist):
        post_edit.refresh_from_db()


def test_private_thread_post_edit_delete_view_deletes_last_post_edit_on_post_in_modal(
    thread_reply_factory, user_client, members_group, user, other_user_private_thread
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    post = thread_reply_factory(other_user_private_thread, poster=user)

    other_post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Other post edit",
        new_content=post.original,
    )
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-post-edit-delete",
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
    assert_contains(response, other_post_edit.old_content)

    with pytest.raises(PostEdit.DoesNotExist):
        post_edit.refresh_from_db()


def test_private_thread_post_edit_delete_view_deletes_last_post_edit_on_post(
    thread_reply_factory, user_client, members_group, user, other_user_private_thread
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    post = thread_reply_factory(other_user_private_thread, poster=user)

    create_post_edit(
        post=post,
        user=user,
        old_content="Previous post edit",
        new_content=post.original,
    )
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )
    create_post_edit(
        post=post,
        user=user,
        old_content="Next post edit",
        new_content=post.original,
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-post-edit-delete",
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
            "page": 2,
        },
    )

    with pytest.raises(PostEdit.DoesNotExist):
        post_edit.refresh_from_db()


def test_private_thread_post_edit_delete_view_deletes_last_post_edit_on_post_in_htmx(
    thread_reply_factory, user_client, members_group, user, other_user_private_thread
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    post = thread_reply_factory(other_user_private_thread, poster=user)

    previous_post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Previous post edit",
        new_content=post.original,
    )
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )
    next_post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Next post edit",
        new_content=post.original,
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-post-edit-delete",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, previous_post_edit.old_content)
    assert_contains(response, next_post_edit.old_content)

    with pytest.raises(PostEdit.DoesNotExist):
        post_edit.refresh_from_db()


def test_private_thread_post_edit_delete_view_deletes_middle_post_edit_on_post_in_modal(
    thread_reply_factory, user_client, members_group, user, other_user_private_thread
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    post = thread_reply_factory(other_user_private_thread, poster=user)

    previous_post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Previous post edit",
        new_content=post.original,
    )
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )
    next_post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Next post edit",
        new_content=post.original,
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-post-edit-delete",
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
    assert_not_contains(response, previous_post_edit.old_content)
    assert_contains(response, next_post_edit.old_content)

    with pytest.raises(PostEdit.DoesNotExist):
        post_edit.refresh_from_db()


def test_private_thread_post_edit_delete_view_shows_confirmation_page_on_get_request(
    thread_reply_factory, user_client, members_group, user, other_user_private_thread
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    post = thread_reply_factory(other_user_private_thread, poster=user)

    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )

    response = user_client.get(
        reverse(
            "misago:private-thread-post-edit-delete",
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
    assert_contains(response, "Are you sure you want to delete this post edit?")


def test_private_thread_post_edit_delete_view_shows_login_required_page_to_anonymous_user(
    client, other_user_private_thread
):
    post = other_user_private_thread.first_post

    response = client.get(
        reverse(
            "misago:private-thread-post-edit-delete",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "post_edit_id": 1,
            },
        ),
    )
    assert_contains(response, "Sign in to view private threads", status_code=401)
