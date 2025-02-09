from django.urls import reverse

from ...attachments.enums import AllowedAttachments
from ...conf.test import override_dynamic_settings
from ...permissions.enums import CanUploadAttachments
from ...test import assert_contains, assert_not_contains


def test_edit_private_thread_view_displays_login_page_to_guests(
    client, user_private_thread
):
    response = client.get(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Sign in to edit posts")


def test_edit_private_thread_view_displays_error_page_to_users_without_private_threads_permission(
    user, user_client, user_private_thread
):
    user.group.can_use_private_threads = False
    user.group.save()

    response = user_client.get(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(
        response,
        "You can&#x27;t use private threads.",
        status_code=403,
    )


def test_edit_private_thread_view_displays_error_page_to_user_who_cant_see_private_thread(
    user_client, private_thread
):
    response = user_client.get(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": private_thread.id,
                "slug": private_thread.slug,
                "post": private_thread.first_post_id,
            },
        )
    )
    assert response.status_code == 404


def test_edit_private_thread_view_displays_error_page_to_user_who_cant_edit_own_threads(
    user, user_client, user_private_thread
):
    user.group.can_edit_own_threads = False
    user.group.save()

    response = user_client.get(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )

    assert_contains(
        response,
        "You can&#x27;t edit threads.",
        status_code=403,
    )


def test_edit_private_thread_view_displays_error_page_to_user_who_cant_edit_own_posts(
    user, user_client, user_private_thread
):
    user.group.can_edit_own_posts = False
    user.group.save()

    response = user_client.get(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )

    assert_contains(
        response,
        "You can&#x27;t edit posts.",
        status_code=403,
    )


def test_edit_private_thread_view_displays_error_page_to_user_trying_to_edit_other_user_thread(
    user_client, other_user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )

    assert_contains(
        response,
        "You can&#x27;t edit other users threads.",
        status_code=403,
    )


def test_edit_private_thread_view_displays_edit_form(user_client, user_private_thread):
    response = user_client.get(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, user_private_thread.first_post.original)


def test_edit_private_thread_view_displays_inline_edit_form_in_htmx(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
        + "?inline=true",
        headers={"hx-request": "true"},
    )
    assert_contains(response, user_private_thread.first_post.original)
    assert_contains(response, "?inline=true")


def test_edit_private_thread_view_displays_edit_form_for_other_user_thread_to_moderator(
    user, user_client, other_user_private_thread, members_group, moderators_group
):
    user.set_groups(members_group, [moderators_group])
    user.save()

    response = user_client.get(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )

    assert_contains(response, "Edit thread")
    assert_contains(response, other_user_private_thread.first_post.original)


def test_edit_private_thread_view_updates_thread_and_post(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert response.status_code == 302

    user_private_thread.refresh_from_db()
    assert user_private_thread.title == "Edited title"

    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"id": user_private_thread.pk, "slug": user_private_thread.slug},
    )

    post = user_private_thread.first_post
    post.refresh_from_db()

    assert post.original == "Edited post"
    assert post.edits == 1


def test_edit_private_thread_view_updates_thread_and_post_in_htmx(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 204

    user_private_thread.refresh_from_db()
    assert user_private_thread.title == "Edited title"

    assert response["hx-redirect"] == reverse(
        "misago:private-thread",
        kwargs={"id": user_private_thread.pk, "slug": user_private_thread.slug},
    )

    post = user_private_thread.first_post
    post.refresh_from_db()

    assert post.original == "Edited post"
    assert post.edits == 1


def test_edit_private_thread_view_updates_thread_and_post_inline_in_htmx(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
        + "?inline=true",
        {
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 204

    user_private_thread.refresh_from_db()
    assert user_private_thread.title == "Edited title"

    assert response["hx-redirect"] == reverse(
        "misago:private-thread",
        kwargs={"id": user_private_thread.pk, "slug": user_private_thread.slug},
    )

    post = user_private_thread.first_post
    post.refresh_from_db()

    assert post.original == "Edited post"
    assert post.edits == 1


def test_edit_private_thread_view_cancels_thread_and_post_edits_inline_in_htmx(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
        + "?inline=true",
        {
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
            "cancel": "true",
        },
        headers={"hx-request": "true"},
    )

    post_original = user_private_thread.first_post.original
    assert_contains(response, post_original)
    assert_contains(
        response,
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
    )
    assert_not_contains(
        response,
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post": user_private_thread.first_post_id,
            },
        ),
    )

    user_private_thread.refresh_from_db()
    assert user_private_thread.title == "User Private Thread"

    post = user_private_thread.first_post
    post.refresh_from_db()

    assert post.original == post_original
    assert post.edits == 0


def test_edit_private_thread_view_previews_message(user_client, user_private_thread):
    response = user_client.post(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posting-post-post": "How's going?", "preview": "true"},
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "Message preview")


def test_edit_private_thread_view_previews_message_in_htmx(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posting-post-post": "How's going?", "preview": "true"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "Message preview")


def test_edit_private_thread_view_previews_message_inline_in_htmx(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
        + "?inline=true",
        {"posting-post-post": "How's going?", "preview": "true"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Message preview")
    assert_contains(response, "?inline=true")


def test_edit_private_thread_view_validates_thread_title(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "posting-title-title": "???",
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "Thread title must include alphanumeric characters.")


def test_edit_private_thread_view_validates_post(user_client, user_private_thread):
    response = user_client.post(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "posting-title-title": "Edited title",
            "posting-post-post": "?",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(
        response, "Posted message must be at least 5 characters long (it has 1)."
    )


def test_edit_private_thread_view_validates_posted_contents(
    user_client, user_private_thread, posted_contents_validator
):
    response = user_client.post(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "posting-title-title": "Edited title",
            "posting-post-post": "This is a spam message",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "Your message contains spam!")


def test_edit_private_thread_view_skips_flood_control(
    user_client, user_private_thread, user_reply
):
    response = user_client.post(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "posting-title-title": "Edited title",
            "posting-post-post": "This is a flood message",
        },
    )
    assert response.status_code == 302

    user_private_thread.refresh_from_db()
    assert user_private_thread.title == "Edited title"

    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"id": user_private_thread.pk, "slug": user_private_thread.slug},
    )

    post = user_private_thread.first_post
    post.refresh_from_db()

    assert post.original == "This is a flood message"
    assert post.edits == 1


def test_edit_private_thread_view_shows_error_if_thread_post_is_accessed(
    user_client, thread
):
    response = user_client.get(
        reverse(
            "misago:edit-private-thread",
            kwargs={"id": thread.id, "slug": thread.slug, "post": thread.first_post_id},
        ),
    )

    assert_not_contains(response, "Edit thread", status_code=404)
    assert_not_contains(response, thread.title, status_code=404)


def test_edit_private_thread_view_displays_attachments_form(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "misago-editor-attachments=")


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE.value)
def test_edit_private_thread_view_hides_attachments_form_if_uploads_are_disabled(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
    )
    assert_contains(response, "Edit thread")
    assert_not_contains(response, "misago-editor-attachments=")


def test_edit_private_thread_view_hides_attachments_form_if_user_has_no_group_permission(
    members_group, user_client, user_private_thread
):
    members_group.can_upload_attachments = CanUploadAttachments.THREADS
    members_group.save()

    response = user_client.get(
        reverse(
            "misago:edit-private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
    )
    assert_contains(response, "Edit thread")
    assert_not_contains(response, "misago-editor-attachments=")
