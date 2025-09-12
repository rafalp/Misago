import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from ...attachments.enums import AllowedAttachments
from ...attachments.models import Attachment
from ...conf.test import override_dynamic_settings
from ...permissions.enums import CanUploadAttachments, CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...test import (
    assert_contains,
    assert_contains_element,
    assert_not_contains,
    assert_not_contains_element,
)


def test_thread_post_edit_view_displays_login_page_to_guests(
    thread_reply_factory, client, thread
):
    post = thread_reply_factory(thread)

    response = client.get(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert_contains(response, "Sign in to edit posts")


def test_thread_post_edit_view_displays_error_404_to_users_without_see_category_permission(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread)

    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.SEE,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert response.status_code == 404


def test_thread_post_edit_view_displays_error_404_to_users_without_browse_category_permission(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread)

    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.BROWSE,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert response.status_code == 404


def test_thread_post_edit_view_displays_error_404_to_users_who_cant_see_thread(
    thread_reply_factory, user_client, hidden_thread
):
    post = thread_reply_factory(hidden_thread)

    response = user_client.get(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": hidden_thread.id,
                "slug": hidden_thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert response.status_code == 404


def test_thread_post_edit_view_displays_error_403_to_users_who_cant_edit_posts(
    thread_reply_factory, user_client, user, members_group, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_edit_own_posts = False
    members_group.save()

    response = user_client.get(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert_contains(response, "You can&#x27;t edit posts.", 403)


def test_thread_post_edit_view_displays_error_403_to_users_who_cant_edit_other_users_posts(
    thread_reply_factory, user_client, other_user, thread
):
    post = thread_reply_factory(thread, poster=other_user)

    response = user_client.get(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert_contains(response, "You can&#x27;t edit other users&#x27; posts.", 403)


def test_thread_post_edit_view_displays_error_403_to_users_who_cant_edit_deleted_users_posts(
    thread_reply_factory, user_client, thread
):
    post = thread_reply_factory(thread)

    response = user_client.get(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert_contains(response, "You can&#x27;t edit other users&#x27; posts.", 403)


def test_thread_post_edit_view_displays_error_403_to_users_who_cant_see_post_contents(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user, is_hidden=True)

    response = user_client.get(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert_contains(response, "You can&#x27;t edit hidden posts.", 403)


def test_thread_post_edit_view_displays_error_403_to_users_without_closed_category_permission(
    thread_reply_factory, user_client, user, default_category, thread
):
    post = thread_reply_factory(thread, poster=user)

    default_category.is_closed = True
    default_category.save()

    response = user_client.get(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert_contains(response, "This category is closed.", 403)


def test_thread_post_edit_view_displays_error_403_to_users_without_closed_thread_permission(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    thread.is_closed = True
    thread.save()

    response = user_client.get(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert_contains(response, "This thread is closed.", 403)


def test_thread_post_edit_view_displays_error_403_to_users_without_protected_post_permission(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user, is_protected=True)

    response = user_client.get(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert_contains(response, "You can&#x27;t edit protected posts.", 403)


def test_thread_post_edit_view_displays_edit_form(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    response = user_client.get(
        reverse(
            "misago:thread-post-edit",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
    )
    assert_contains(response, "Edit post")
    assert_contains(response, thread.title)
    assert_contains(response, post.original)


def test_thread_post_edit_view_displays_edit_form_for_moderator(
    thread_reply_factory, moderator_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    response = moderator_client.get(
        reverse(
            "misago:thread-post-edit",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
    )
    assert_contains(response, "Edit post")
    assert_contains(response, thread.title)
    assert_contains(response, post.original)


def test_thread_post_edit_view_displays_inline_edit_form_in_htmx(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    response = user_client.get(
        reverse(
            "misago:thread-post-edit",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
        + "?inline=true",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Save")
    assert_contains(response, post.original)
    assert_contains(response, "?inline=true")
