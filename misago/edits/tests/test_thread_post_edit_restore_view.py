from django.urls import reverse

from ...permissions.enums import CanSeePostEdits, CategoryPermission
from ...permissions.models import CategoryGroupPermission
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


def test_thread_post_edit_restore_view_shows_error_403_if_post_edit_cant_be_restored(
    user_client, user, thread, user_reply
):
    post_edit = create_post_edit(post=user_reply, user=user)

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
        response,
        "You can&#x27;t restore the post from this edit.",
        status_code=403,
    )


def test_thread_post_edit_restore_view_shows_error_403_if_post_is_not_editable(
    user_client, user, thread, user_reply
):
    thread.is_closed = True
    thread.save()

    post_edit = create_post_edit(
        post=user_reply,
        user=user,
        old_content="Lorem ipsum",
        new_content="Dolor met",
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
    assert_contains(response, "This thread is locked.", status_code=403)


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


def test_thread_post_edit_restore_view_returns_error_404_if_thread_doesnt_exist(
    user_client,
):
    response = user_client.get(
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": 1,
                "slug": "doesnt-exist",
                "post_id": 1,
                "post_edit_id": 1,
            },
        ),
    )
    assert response.status_code == 404


def test_thread_post_edit_restore_view_returns_error_404_if_user_cant_see_thread_category(
    thread_reply_factory, user_client, members_group, user, thread
):
    CategoryGroupPermission.objects.filter(
        group=members_group,
        permission=CategoryPermission.SEE,
    ).delete()

    post = thread_reply_factory(thread, poster=user)
    post_edit = create_post_edit(post=post, user=user)

    response = user_client.get(
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )
    assert response.status_code == 404


def test_thread_post_edit_restore_view_returns_error_404_if_user_cant_browse_thread_category(
    thread_reply_factory, user_client, members_group, user, thread
):
    CategoryGroupPermission.objects.filter(
        group=members_group,
        permission=CategoryPermission.BROWSE,
    ).delete()

    post = thread_reply_factory(thread, poster=user)
    post_edit = create_post_edit(post=post, user=user)

    response = user_client.get(
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )
    assert response.status_code == 404


def test_thread_post_edit_restore_view_returns_error_404_if_user_cant_see_thread(
    thread_reply_factory, user_client, user, thread
):
    thread.is_hidden = True
    thread.save()

    post = thread_reply_factory(thread, poster=user)
    post_edit = create_post_edit(post=post, user=user)

    response = user_client.get(
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )
    assert response.status_code == 404


def test_thread_post_edit_restore_view_returns_error_404_if_thread_post_doesnt_exist(
    user_client, thread
):
    response = user_client.get(
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": 1,
                "post_edit_id": 1,
            },
        ),
    )
    assert response.status_code == 404


def test_thread_post_edit_restore_view_returns_error_404_if_thread_post_belongs_to_other_thread(
    user_client, thread, other_thread
):
    response = user_client.get(
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": other_thread.first_post_id,
                "post_edit_id": 1,
            },
        ),
    )
    assert response.status_code == 404


def test_thread_post_edit_restore_view_returns_error_404_if_user_cant_see_thread_post(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, is_unapproved=True)
    post_edit = create_post_edit(post=post, user=user)

    response = user_client.get(
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )
    assert response.status_code == 404


def test_thread_post_edit_restore_view_returns_error_403_if_user_cant_see_thread_post_contents(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, is_hidden=True)
    post_edit = create_post_edit(post=post, user=user)

    response = user_client.get(
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )
    assert_contains(
        response, "You can&#x27;t see this post&#x27;s contents.", status_code=403
    )


def test_thread_post_edit_restore_view_returns_error_403_if_user_cant_see_other_users_post_edits_history(
    thread_reply_factory, user_client, members_group, user, thread
):
    members_group.can_see_others_post_edits = CanSeePostEdits.NEVER
    members_group.save()

    post = thread_reply_factory(thread)
    post_edit = create_post_edit(post=post, user=user)

    response = user_client.get(
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )
    assert_contains(
        response, "You can&#x27;t see this post&#x27;s edit history.", status_code=403
    )


def test_thread_post_edit_restore_view_returns_error_403_if_user_can_see_other_users_post_edits_count_only(
    thread_reply_factory, user_client, members_group, user, thread
):
    members_group.can_see_others_post_edits = CanSeePostEdits.COUNT
    members_group.save()

    post = thread_reply_factory(thread)
    post_edit = create_post_edit(post=post, user=user)

    response = user_client.get(
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )
    assert_contains(
        response, "You can&#x27;t see this post&#x27;s edit history.", status_code=403
    )


def test_thread_post_edit_restore_view_returns_error_404_if_post_is_in_thread(
    thread_reply_factory, user_client, user, other_user_private_thread
):
    post = thread_reply_factory(other_user_private_thread)
    post_edit = create_post_edit(post=post, user=user)

    response = user_client.get(
        reverse(
            "misago:thread-post-edit-restore",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
                "post_edit_id": post_edit.id,
            },
        ),
    )
    assert response.status_code == 404
