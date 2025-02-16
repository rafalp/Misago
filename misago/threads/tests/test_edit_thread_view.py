import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from ...attachments.enums import AllowedAttachments
from ...attachments.models import Attachment
from ...conf.test import override_dynamic_settings
from ...permissions.enums import CanUploadAttachments, CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...posting.forms import PostForm
from ...posting.formsets import PostingFormset
from ...test import (
    assert_contains,
    assert_contains_element,
    assert_not_contains,
    assert_not_contains_element,
)


def test_edit_thread_view_displays_login_page_to_guests(client, user_thread):
    response = client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
    )
    assert_contains(response, "Sign in to edit posts")


def test_edit_thread_view_displays_error_page_to_user_who_cant_see_thread_category(
    user, user_client, user_thread
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.SEE,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
    )
    assert response.status_code == 404


def test_edit_thread_view_displays_error_page_to_user_who_cant_browse_thread_category(
    user, user_client, user_thread
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.BROWSE,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
    )
    assert response.status_code == 404


def test_edit_thread_view_displays_error_page_to_user_who_cant_edit_in_closed_category(
    user_client, user_thread
):
    user_thread.category.is_closed = True
    user_thread.category.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
    )

    assert_contains(
        response,
        "This category is closed.",
        status_code=403,
    )


def test_edit_thread_view_displays_error_page_to_user_who_cant_edit_in_closed_thread(
    user_client, user_thread
):
    user_thread.is_closed = True
    user_thread.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
    )

    assert_contains(
        response,
        "This thread is closed.",
        status_code=403,
    )


def test_edit_thread_view_displays_error_page_to_user_who_cant_edit_protected_post(
    user_client, user_thread
):
    post = user_thread.first_post
    post.is_protected = True
    post.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
    )

    assert_contains(
        response,
        "You can&#x27;t edit protected posts.",
        status_code=403,
    )


def test_edit_thread_view_displays_error_page_to_user_who_cant_edit_own_threads(
    user, user_client, user_thread
):
    user.group.can_edit_own_threads = False
    user.group.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
    )

    assert_contains(
        response,
        "You can&#x27;t edit threads.",
        status_code=403,
    )


def test_edit_thread_view_displays_error_page_to_user_who_cant_edit_own_posts(
    user, user_client, user_thread
):
    user.group.can_edit_own_posts = False
    user.group.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
    )

    assert_contains(
        response,
        "You can&#x27;t edit posts.",
        status_code=403,
    )


def test_edit_thread_view_displays_error_page_to_user_trying_to_edit_other_user_thread(
    user_client, other_user_thread, other_user
):

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": other_user_thread.id, "slug": other_user_thread.slug},
        )
    )

    assert_contains(
        response,
        "You can&#x27;t edit other users threads.",
        status_code=403,
    )


def test_edit_thread_view_displays_edit_form(user_client, user_thread):
    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, user_thread.first_post.original)


def test_edit_thread_view_displays_inline_edit_form_in_htmx(user_client, user_thread):
    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
        + "?inline=true",
        headers={"hx-request": "true"},
    )
    assert_contains(response, user_thread.first_post.original)
    assert_contains(response, "?inline=true")


def test_edit_thread_view_displays_edit_form_in_closed_category_to_moderator(
    user, user_client, user_thread, members_group, moderators_group
):
    user_thread.category.is_closed = True
    user_thread.category.save()

    user.set_groups(members_group, [moderators_group])
    user.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
    )

    assert_contains(response, "Edit thread")
    assert_contains(response, user_thread.first_post.original)


def test_edit_thread_view_displays_edit_form_in_closed_thread_to_moderator(
    user, user_client, user_thread, members_group, moderators_group
):
    user_thread.is_closed = True
    user_thread.save()

    user.set_groups(members_group, [moderators_group])
    user.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
    )

    assert_contains(response, "Edit thread")
    assert_contains(response, user_thread.first_post.original)


def test_edit_thread_view_displays_edit_form_for_protected_post_to_moderator(
    user, user_client, user_thread, members_group, moderators_group
):
    post = user_thread.first_post
    post.is_protected = True
    post.save()

    user.set_groups(members_group, [moderators_group])
    user.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
    )

    assert_contains(response, "Edit thread")
    assert_contains(response, user_thread.first_post.original)


def test_edit_thread_view_displays_edit_form_for_other_user_thread_to_moderator(
    user, user_client, other_user_thread, members_group, moderators_group
):
    user.set_groups(members_group, [moderators_group])
    user.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": other_user_thread.id, "slug": other_user_thread.slug},
        )
    )

    assert_contains(response, "Edit thread")
    assert_contains(response, other_user_thread.first_post.original)


def test_edit_thread_view_updates_thread_and_post(user_client, user_thread):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert response.status_code == 302

    user_thread.refresh_from_db()
    assert user_thread.title == "Edited title"

    assert response["location"] == reverse(
        "misago:thread",
        kwargs={"id": user_thread.pk, "slug": user_thread.slug},
    )

    post = user_thread.first_post
    post.refresh_from_db()

    assert post.original == "Edited post"
    assert post.edits == 1


def test_edit_thread_view_updates_thread_and_post_in_htmx(user_client, user_thread):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 204

    user_thread.refresh_from_db()
    assert user_thread.title == "Edited title"

    assert response["hx-redirect"] == reverse(
        "misago:thread",
        kwargs={"id": user_thread.pk, "slug": user_thread.slug},
    )

    post = user_thread.first_post
    post.refresh_from_db()

    assert post.original == "Edited post"
    assert post.edits == 1


def test_edit_thread_view_updates_thread_and_post_inline_in_htmx(
    user_client, user_thread
):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
        + "?inline=true",
        {
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 204

    user_thread.refresh_from_db()
    assert user_thread.title == "Edited title"

    assert response["hx-redirect"] == reverse(
        "misago:thread",
        kwargs={"id": user_thread.pk, "slug": user_thread.slug},
    )

    post = user_thread.first_post
    post.refresh_from_db()

    assert post.original == "Edited post"
    assert post.edits == 1


def test_edit_thread_view_cancels_thread_and_post_edits_inline_in_htmx(
    user_client, user_thread
):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
        + "?inline=true",
        {
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
            "cancel": "true",
        },
        headers={"hx-request": "true"},
    )

    post_original = user_thread.first_post.original
    assert_contains(response, post_original)
    assert_contains(
        response,
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
            },
        ),
    )
    assert_not_contains(
        response,
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        ),
    )

    user_thread.refresh_from_db()
    assert user_thread.title == "Test thread"

    post = user_thread.first_post
    post.refresh_from_db()

    assert post.original == post_original
    assert post.edits == 0


def test_edit_thread_view_previews_message(user_client, user_thread):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "posting-post-post": "How's going?",
            PostingFormset.preview_action: "true",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "Message preview")


def test_edit_thread_view_previews_message_in_htmx(user_client, user_thread):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "posting-post-post": "How's going?",
            PostingFormset.preview_action: "true",
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "Message preview")


def test_edit_thread_view_previews_message_inline_in_htmx(user_client, user_thread):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        )
        + "?inline=true",
        {
            "posting-post-post": "How's going?",
            PostingFormset.preview_action: "true",
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Message preview")
    assert_contains(response, "?inline=true")


def test_edit_thread_view_validates_thread_title(user_client, user_thread):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "posting-title-title": "???",
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "Thread title must include alphanumeric characters.")


def test_edit_thread_view_validates_post(user_client, user_thread):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
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


def test_edit_thread_view_validates_posted_contents(
    user_client, user_thread, posted_contents_validator
):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "posting-title-title": "Edited title",
            "posting-post-post": "This is a spam message",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "Your message contains spam!")


def test_edit_thread_view_skips_flood_control(user_client, user_thread, user_reply):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "posting-title-title": "Edited title",
            "posting-post-post": "This is a flood message",
        },
    )
    assert response.status_code == 302

    user_thread.refresh_from_db()
    assert user_thread.title == "Edited title"

    assert response["location"] == reverse(
        "misago:thread",
        kwargs={"id": user_thread.pk, "slug": user_thread.slug},
    )

    post = user_thread.first_post
    post.refresh_from_db()

    assert post.original == "This is a flood message"
    assert post.edits == 1


def test_edit_thread_view_shows_error_if_private_thread_post_is_accessed(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
    )

    assert_not_contains(response, "Edit thread", status_code=404)
    assert_not_contains(response, user_private_thread.title, status_code=404)


def test_edit_thread_view_displays_attachments_form(user_client, user_thread):
    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
            },
        ),
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "misago-editor-attachments=")


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE.value)
def test_edit_thread_view_hides_attachments_form_if_uploads_are_disabled(
    user_client, user_thread
):
    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
            },
        ),
    )
    assert_contains(response, "Edit thread")
    assert_not_contains(response, "misago-editor-attachments=")


def test_edit_thread_view_hides_attachments_form_if_user_has_no_group_permission(
    members_group, user_client, user_thread
):
    members_group.can_upload_attachments = CanUploadAttachments.NEVER
    members_group.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
            },
        ),
    )
    assert_contains(response, "Edit thread")
    assert_not_contains(response, "misago-editor-attachments=")


def test_edit_thread_view_uploads_attachment_on_submit(
    user, user_client, user_thread, teardown_attachments
):
    assert not Attachment.objects.exists()

    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
            },
        ),
        {
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
            "posting-post-upload": [
                SimpleUploadedFile("test.txt", b"Hello world!", "text/plain"),
            ],
        },
    )
    assert response.status_code == 302

    attachment = Attachment.objects.get(uploader=user)
    assert attachment.category_id == user_thread.category_id
    assert attachment.thread_id == user_thread.id
    assert attachment.post_id == user_thread.first_post_id
    assert attachment.uploader_id == user.id
    assert not attachment.is_deleted
    assert attachment.name == "test.txt"


@pytest.mark.parametrize(
    "action_name", (PostingFormset.preview_action, PostForm.upload_action)
)
def test_edit_thread_view_uploads_attachment_on_preview_or_upload(
    action_name, user, user_client, user_thread, teardown_attachments
):
    assert not Attachment.objects.exists()

    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            action_name: "true",
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
            "posting-post-upload": [
                SimpleUploadedFile("test.txt", b"Hello world!", "text/plain"),
            ],
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "misago-editor-attachments=")

    attachment = Attachment.objects.get(uploader=user)
    assert attachment.category_id is None
    assert attachment.thread_id is None
    assert attachment.post_id is None
    assert attachment.uploader_id == user.id
    assert not attachment.is_deleted
    assert attachment.name == "test.txt"

    assert_contains(response, attachment.name)
    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.attachment_ids_field,
        value=attachment.id,
    )


@pytest.mark.parametrize(
    "action_name", (PostingFormset.preview_action, PostForm.upload_action)
)
def test_edit_thread_view_displays_image_attachment(
    action_name, user_client, user_thread, user_image_attachment
):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_image_attachment.id)],
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "misago-editor-attachments=")

    assert_contains(response, user_image_attachment.name)
    assert_contains(response, user_image_attachment.get_absolute_url())
    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.attachment_ids_field,
        value=user_image_attachment.id,
    )


@pytest.mark.parametrize(
    "action_name", (PostingFormset.preview_action, PostForm.upload_action)
)
def test_edit_thread_view_displays_image_with_thumbnail_attachment(
    action_name, user_client, user_thread, user_image_thumbnail_attachment
):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_image_thumbnail_attachment.id)],
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "misago-editor-attachments=")

    assert_contains(response, user_image_thumbnail_attachment.name)
    assert_contains(response, user_image_thumbnail_attachment.get_thumbnail_url())
    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.attachment_ids_field,
        value=user_image_thumbnail_attachment.id,
    )


@pytest.mark.parametrize(
    "action_name", (PostingFormset.preview_action, PostForm.upload_action)
)
def test_edit_thread_view_displays_video_attachment(
    action_name, user_client, user_thread, user_video_attachment
):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_video_attachment.id)],
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "misago-editor-attachments=")

    assert_contains(response, user_video_attachment.name)
    assert_contains(response, user_video_attachment.get_absolute_url())
    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.attachment_ids_field,
        value=user_video_attachment.id,
    )


@pytest.mark.parametrize(
    "action_name", (PostingFormset.preview_action, PostForm.upload_action)
)
def test_edit_thread_view_displays_file_attachment(
    action_name, user_client, user_thread, user_text_attachment
):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "misago-editor-attachments=")

    assert_contains(response, user_text_attachment.name)
    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.attachment_ids_field,
        value=user_text_attachment.id,
    )


def test_edit_thread_view_associates_unused_attachment_on_submit(
    user_client, user_thread, user_text_attachment
):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert response.status_code == 302

    user_thread.refresh_from_db()
    assert response["location"] == reverse(
        "misago:thread", kwargs={"id": user_thread.pk, "slug": user_thread.slug}
    )

    user_text_attachment.refresh_from_db()
    assert user_text_attachment.category_id == user_thread.category_id
    assert user_text_attachment.thread_id == user_thread.id
    assert user_text_attachment.post_id == user_thread.first_post_id
    assert not user_text_attachment.is_deleted


def test_edit_thread_view_adds_attachment_to_deleted_list(
    user_client, user_thread, user_text_attachment
):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            PostForm.delete_attachment_field: str(user_text_attachment.id),
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "misago-editor-attachments=")

    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.attachment_ids_field,
        value=user_text_attachment.id,
    )
    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.deleted_attachment_ids_field,
        value=user_text_attachment.id,
    )
    assert_not_contains(response, user_text_attachment.name)
    assert_not_contains(response, user_text_attachment.get_absolute_url())


@pytest.mark.parametrize(
    "action_name", (PostingFormset.preview_action, PostForm.upload_action)
)
def test_edit_thread_view_maintains_deleted_attachments_list(
    action_name, user_client, user_thread, user_text_attachment
):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            PostForm.deleted_attachment_ids_field: [str(user_text_attachment.id)],
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "misago-editor-attachments=")

    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.attachment_ids_field,
        value=user_text_attachment.id,
    )
    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.deleted_attachment_ids_field,
        value=user_text_attachment.id,
    )
    assert_not_contains(response, user_text_attachment.name)
    assert_not_contains(response, user_text_attachment.get_absolute_url())


def test_edit_thread_view_deletes_attachment_on_submit(
    user_client, user_thread, user_text_attachment
):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            PostForm.deleted_attachment_ids_field: [str(user_text_attachment.id)],
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert response.status_code == 302

    user_thread.refresh_from_db()
    assert response["location"] == reverse(
        "misago:thread", kwargs={"id": user_thread.pk, "slug": user_thread.slug}
    )

    user_text_attachment.refresh_from_db()
    assert user_text_attachment.category_id is None
    assert user_text_attachment.thread_id is None
    assert user_text_attachment.post_id is None
    assert user_text_attachment.is_deleted


def test_edit_thread_view_displays_associated_attachment(
    user_client, user_thread, text_attachment
):
    text_attachment.associate_with_post(user_thread.first_post)
    text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "misago-editor-attachments=")
    assert_contains_element(response, "input", type="file", name="posting-post-upload")

    assert_contains(response, text_attachment.name)
    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.attachment_ids_field,
        value=text_attachment.id,
    )


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE.value)
def test_edit_thread_view_displays_associated_attachment_if_uploads_are_disabled(
    user_client, user_thread, text_attachment
):
    text_attachment.associate_with_post(user_thread.first_post)
    text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "misago-editor-attachments=")
    assert_not_contains_element(
        response, "input", type="file", name="posting-post-upload"
    )

    assert_contains(response, text_attachment.name)
    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.attachment_ids_field,
        value=text_attachment.id,
    )


def test_edit_thread_view_displays_associated_attachment_for_user_without_upload_permission(
    members_group, user_client, user_thread, text_attachment
):
    members_group.can_upload_attachments = CanUploadAttachments.NEVER
    members_group.save()

    text_attachment.associate_with_post(user_thread.first_post)
    text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "misago-editor-attachments=")
    assert_not_contains_element(
        response, "input", type="file", name="posting-post-upload"
    )

    assert_contains(response, text_attachment.name)
    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.attachment_ids_field,
        value=text_attachment.id,
    )


def test_edit_thread_view_adds_existing_attachment_to_deleted_list(
    user_client, user_thread, text_attachment
):
    text_attachment.associate_with_post(user_thread.first_post)
    text_attachment.save()

    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            PostForm.attachment_ids_field: [str(text_attachment.id)],
            PostForm.delete_attachment_field: str(text_attachment.id),
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "misago-editor-attachments=")
    assert_contains_element(response, "input", type="file", name="posting-post-upload")

    assert_not_contains(response, text_attachment.name)
    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.attachment_ids_field,
        value=text_attachment.id,
    )
    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.deleted_attachment_ids_field,
        value=text_attachment.id,
    )


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE.value)
def test_edit_thread_view_adds_existing_attachment_to_deleted_list_if_uploads_are_disabled(
    user_client, user_thread, text_attachment
):
    text_attachment.associate_with_post(user_thread.first_post)
    text_attachment.save()

    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            PostForm.attachment_ids_field: [str(text_attachment.id)],
            PostForm.delete_attachment_field: str(text_attachment.id),
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "misago-editor-attachments=")
    assert_not_contains_element(
        response, "input", type="file", name="posting-post-upload"
    )

    assert_not_contains(response, text_attachment.name)
    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.attachment_ids_field,
        value=text_attachment.id,
    )
    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.deleted_attachment_ids_field,
        value=text_attachment.id,
    )


def test_edit_thread_view_adds_existing_attachment_to_deleted_list_for_user_without_upload_permission(
    members_group, user_client, user_thread, text_attachment
):
    members_group.can_upload_attachments = CanUploadAttachments.NEVER
    members_group.save()

    text_attachment.associate_with_post(user_thread.first_post)
    text_attachment.save()

    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            PostForm.attachment_ids_field: [str(text_attachment.id)],
            PostForm.delete_attachment_field: str(text_attachment.id),
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "misago-editor-attachments=")
    assert_not_contains_element(
        response, "input", type="file", name="posting-post-upload"
    )

    assert_not_contains(response, text_attachment.name)
    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.attachment_ids_field,
        value=text_attachment.id,
    )
    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.deleted_attachment_ids_field,
        value=text_attachment.id,
    )


def test_edit_thread_view_deletes_existing_attachment_on_submit(
    user_client, user_thread, text_attachment
):
    text_attachment.associate_with_post(user_thread.first_post)
    text_attachment.save()

    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            PostForm.attachment_ids_field: [str(text_attachment.id)],
            PostForm.deleted_attachment_ids_field: [str(text_attachment.id)],
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert response.status_code == 302

    user_thread.refresh_from_db()
    assert response["location"] == reverse(
        "misago:thread", kwargs={"id": user_thread.pk, "slug": user_thread.slug}
    )

    text_attachment.refresh_from_db()
    assert text_attachment.category_id is None
    assert text_attachment.thread_id is None
    assert text_attachment.post_id is None
    assert text_attachment.is_deleted


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE.value)
def test_edit_thread_view_deletes_existing_attachment_on_submit_if_uploads_are_disabled(
    user_client, user_thread, text_attachment
):
    text_attachment.associate_with_post(user_thread.first_post)
    text_attachment.save()

    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            PostForm.attachment_ids_field: [str(text_attachment.id)],
            PostForm.deleted_attachment_ids_field: [str(text_attachment.id)],
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert response.status_code == 302

    user_thread.refresh_from_db()
    assert response["location"] == reverse(
        "misago:thread", kwargs={"id": user_thread.pk, "slug": user_thread.slug}
    )

    text_attachment.refresh_from_db()
    assert text_attachment.category_id is None
    assert text_attachment.thread_id is None
    assert text_attachment.post_id is None
    assert text_attachment.is_deleted


def test_edit_thread_view_deletes_existing_attachment_on_submit_for_user_without_upload_permission(
    members_group, user_client, user_thread, text_attachment
):
    members_group.can_upload_attachments = CanUploadAttachments.NEVER
    members_group.save()

    text_attachment.associate_with_post(user_thread.first_post)
    text_attachment.save()

    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            PostForm.attachment_ids_field: [str(text_attachment.id)],
            PostForm.deleted_attachment_ids_field: [str(text_attachment.id)],
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert response.status_code == 302

    user_thread.refresh_from_db()
    assert response["location"] == reverse(
        "misago:thread", kwargs={"id": user_thread.pk, "slug": user_thread.slug}
    )

    text_attachment.refresh_from_db()
    assert text_attachment.category_id is None
    assert text_attachment.thread_id is None
    assert text_attachment.post_id is None
    assert text_attachment.is_deleted


def test_edit_thread_view_embeds_attachments_in_preview(
    user_client, user_thread, user_image_attachment
):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            PostingFormset.preview_action: "true",
            PostForm.attachment_ids_field: [str(user_image_attachment.id)],
            "posting-title-title": "Edited title",
            "posting-post-post": (
                f"Edit: <attachment={user_image_attachment.name}:{user_image_attachment.id}>"
            ),
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "Message preview")
    assert_contains_element(response, "a", href=user_image_attachment.get_details_url())
    assert_contains_element(
        response, "img", src=user_image_attachment.get_absolute_url()
    )
