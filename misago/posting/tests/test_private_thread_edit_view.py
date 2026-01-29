from unittest.mock import ANY

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from ...attachments.enums import AllowedAttachments
from ...attachments.models import Attachment
from ...conf.test import override_dynamic_settings
from ...edits.models import PostEdit
from ...permissions.enums import CanUploadAttachments
from ...threadupdates.enums import ThreadUpdateActionName
from ...threadupdates.models import ThreadUpdate
from ...test import (
    assert_contains,
    assert_contains_element,
    assert_not_contains,
    assert_not_contains_element,
)
from ..forms import PostForm
from ..formsets import Formset


def test_private_thread_edit_view_displays_login_required_page_to_anonymous_user(
    client, user_private_thread
):
    response = client.get(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Sign in to edit threads", status_code=401)


def test_private_thread_edit_view_shows_error_403_to_users_without_private_threads_permission(
    user_client, members_group, user_private_thread
):
    members_group.can_use_private_threads = False
    members_group.save()

    response = user_client.get(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "You can&#x27;t use private threads.", 403)


def test_private_thread_edit_view_shows_error_404_to_users_who_cant_see_thread(
    user_client, private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": private_thread.id,
                "slug": private_thread.slug,
            },
        )
    )
    assert response.status_code == 404


def test_private_thread_edit_view_shows_error_403_to_users_who_cant_edit_threads(
    user_client, members_group, user_private_thread
):
    members_group.can_edit_own_threads = False
    members_group.save()

    response = user_client.get(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "You can&#x27;t edit threads.", 403)


def test_private_thread_edit_view_shows_error_403_to_users_who_cant_edit_other_users_threads(
    user_client, other_user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "You can&#x27;t edit other users&#x27; threads.", 403)


def test_private_thread_edit_view_displays_edit_form(user_client, user_private_thread):
    response = user_client.get(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, user_private_thread.title)
    assert_contains(response, user_private_thread.first_post.original)


def test_private_thread_edit_view_displays_edit_form_for_moderator(
    moderator_client, user_private_thread
):
    response = moderator_client.get(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, user_private_thread.title)
    assert_contains(response, user_private_thread.first_post.original)


def test_private_thread_edit_view_displays_inline_edit_form_in_htmx(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
        + "?inline=true",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Save")
    assert_contains(response, user_private_thread.title)
    assert_contains(response, user_private_thread.first_post.original)
    assert_contains(response, "?inline=true")


def test_private_thread_edit_view_updates_thread_title_and_post(
    user_client, user, user_private_thread
):
    old_title = user_private_thread.title

    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
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
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )
    assert user_private_thread.title == "Edited title"

    post = user_private_thread.first_post
    assert post.original == "Edited post"
    assert post.updated_at
    assert post.edits == 1
    assert post.last_editor == user
    assert post.last_editor_name == user.username
    assert post.last_editor_slug == user.slug
    assert post.last_edit_reason is None

    post_edit = PostEdit.objects.get(post=post)
    assert post_edit.old_title == old_title
    assert post_edit.new_title == "Edited title"
    assert post_edit.added_content == 1
    assert post_edit.removed_content == 1
    assert post_edit.attachments == []
    assert post_edit.added_attachments == 0
    assert post_edit.removed_attachments == 0


def test_private_thread_edit_view_updates_thread_title_and_post_in_htmx(
    user_client, user, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
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
    assert response["hx-redirect"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )
    assert user_private_thread.title == "Edited title"

    post = user_private_thread.first_post
    assert post.original == "Edited post"
    assert post.updated_at
    assert post.edits == 1
    assert post.last_editor == user
    assert post.last_editor_name == user.username
    assert post.last_editor_slug == user.slug
    assert post.last_edit_reason is None


def test_private_thread_edit_view_updates_thread_title_and_post_inline_in_htmx(
    user_client, user, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
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
    assert response["hx-redirect"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )
    assert user_private_thread.title == "Edited title"

    post = user_private_thread.first_post
    assert post.original == "Edited post"
    assert post.updated_at
    assert post.edits == 1
    assert post.last_editor == user
    assert post.last_editor_name == user.username
    assert post.last_editor_slug == user.slug
    assert post.last_edit_reason is None


def test_private_thread_edit_view_sets_edit_reason(
    user_client, user, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
            "posting-edit-reason-edit_reason": "Lorem ipsum dolor met",
        },
    )
    assert response.status_code == 302

    post = user_private_thread.first_post
    post.refresh_from_db()
    assert post.original == "Edited post"
    assert post.updated_at
    assert post.edits == 1
    assert post.last_editor == user
    assert post.last_editor_name == user.username
    assert post.last_editor_slug == user.slug
    assert post.last_edit_reason == "Lorem ipsum dolor met"

    post_edit = PostEdit.objects.get(post=post)
    assert post_edit.edit_reason == "Lorem ipsum dolor met"


def test_private_thread_edit_view_creates_changed_title_update_object(
    user_client, user, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert response.status_code == 302

    ThreadUpdate.objects.get(
        category=user_private_thread.category,
        thread=user_private_thread,
        actor=user,
        action=ThreadUpdateActionName.CHANGED_TITLE,
        context=user_private_thread.title,
    )


def test_private_thread_edit_view_doesnt_create_changed_title_update_object_if_title_wasnt_changed(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "posting-title-title": user_private_thread.title,
            "posting-post-post": "Edited post",
        },
    )
    assert response.status_code == 302

    assert not ThreadUpdate.objects.exists()


def test_private_thread_edit_view_previews_message(user_client, user_private_thread):
    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            Formset.preview_action: "true",
            "posting-post-post": "How is going?",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, user_private_thread.title)
    assert_contains(response, "Message preview")
    assert_contains(response, "<p>How is going?</p>")


def test_private_thread_edit_view_previews_message_in_htmx(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            Formset.preview_action: "true",
            "posting-post-post": "How is going?",
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, "Message preview")
    assert_contains(response, "<p>How is going?</p>")


def test_private_thread_edit_view_previews_message_inline_in_htmx(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
        + "?inline=true",
        {
            Formset.preview_action: "true",
            "posting-post-post": "How is going?",
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Message preview")
    assert_contains(response, "<p>How is going?</p>")
    assert_contains(response, "?inline=true")


def test_private_thread_edit_view_validates_thread_title(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "posting-title-title": "???",
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, user_private_thread.title)
    assert_contains(response, "Thread title must include alphanumeric characters.")


def test_private_thread_edit_view_validates_post(user_client, user_private_thread):
    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "posting-title-title": "Edited title",
            "posting-post-post": "?",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, user_private_thread.title)
    assert_contains(
        response, "Posted message must be at least 5 characters long (it has 1)."
    )


def test_private_thread_edit_view_validates_posted_contents(
    user_client, user_private_thread, posted_contents_validator
):
    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "posting-title-title": "Edited title",
            "posting-post-post": "This is a spam message",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, user_private_thread.title)
    assert_contains(response, "Your message contains spam!")


def test_private_thread_edit_view_skips_flood_control(
    user_client, user_private_thread, user_reply
):
    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
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
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )

    post = user_private_thread.first_post
    post.refresh_from_db()

    assert post.original == "This is a flood message"
    assert post.edits == 1


def test_private_thread_edit_view_displays_attachments_form(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, user_private_thread.title)
    assert_contains(response, "misago-editor-attachments=")


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE.value)
def test_private_thread_edit_view_hides_attachments_form_if_uploads_are_disabled(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, user_private_thread.title)
    assert_not_contains(response, "misago-editor-attachments=")


def test_private_thread_edit_view_hides_attachments_form_if_user_has_no_group_permission(
    members_group, user_client, user_private_thread
):
    members_group.can_upload_attachments = CanUploadAttachments.THREADS
    members_group.save()

    response = user_client.get(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, user_private_thread.title)
    assert_not_contains(response, "misago-editor-attachments=")


def test_private_thread_edit_view_uploads_attachment_on_submit(
    user, user_client, user_private_thread, teardown_attachments
):
    assert not Attachment.objects.exists()

    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
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
    assert attachment.category_id == user_private_thread.category_id
    assert attachment.thread_id == user_private_thread.id
    assert attachment.post_id == user_private_thread.first_post_id
    assert attachment.uploader_id == user.id
    assert not attachment.is_deleted
    assert attachment.name == "test.txt"

    post_edit = PostEdit.objects.get(post=user_private_thread.first_post.id)
    assert post_edit.attachments == [
        {
            "id": attachment.id,
            "uploader_id": attachment.uploader_id,
            "uploader_name": attachment.uploader_name,
            "uploader_slug": attachment.uploader_slug,
            "uploaded_at": ANY,
            "name": attachment.name,
            "slug": attachment.slug,
            "filetype_id": attachment.filetype_id,
            "dimensions": None,
            "thumbnail": None,
            "size": attachment.size,
            "change": "+",
        },
    ]
    assert post_edit.added_attachments == 1
    assert post_edit.removed_attachments == 0


@pytest.mark.parametrize(
    "action_name", (Formset.preview_action, PostForm.upload_action)
)
def test_private_thread_edit_view_uploads_attachment_on_preview_or_upload(
    action_name, user, user_client, user_private_thread, teardown_attachments
):
    assert not Attachment.objects.exists()

    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
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
    assert_contains(response, user_private_thread.title)
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
    "action_name", (Formset.preview_action, PostForm.upload_action)
)
def test_private_thread_edit_view_displays_image_attachment(
    action_name, user_client, user_private_thread, user_image_attachment
):
    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_image_attachment.id)],
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, user_private_thread.title)
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
    "action_name", (Formset.preview_action, PostForm.upload_action)
)
def test_private_thread_edit_view_displays_image_with_thumbnail_attachment(
    action_name, user_client, user_private_thread, user_image_thumbnail_attachment
):
    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_image_thumbnail_attachment.id)],
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, user_private_thread.title)
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
    "action_name", (Formset.preview_action, PostForm.upload_action)
)
def test_private_thread_edit_view_displays_video_attachment(
    action_name, user_client, user_private_thread, user_video_attachment
):
    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_video_attachment.id)],
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, user_private_thread.title)
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
    "action_name", (Formset.preview_action, PostForm.upload_action)
)
def test_private_thread_edit_view_displays_file_attachment(
    action_name, user_client, user_private_thread, user_text_attachment
):
    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, user_private_thread.title)
    assert_contains(response, "misago-editor-attachments=")

    assert_contains(response, user_text_attachment.name)
    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.attachment_ids_field,
        value=user_text_attachment.id,
    )


def test_private_thread_edit_view_associates_unused_attachment_on_submit(
    user_client, user_private_thread, user_text_attachment
):
    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert response.status_code == 302

    user_private_thread.refresh_from_db()
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )

    attachment_uploaded_at = user_text_attachment.uploaded_at

    user_text_attachment.refresh_from_db()
    assert user_text_attachment.category_id == user_private_thread.category_id
    assert user_text_attachment.thread_id == user_private_thread.id
    assert user_text_attachment.post_id == user_private_thread.first_post_id
    assert not user_text_attachment.is_deleted

    post_edit = PostEdit.objects.get(post=user_private_thread.first_post.id)
    assert post_edit.attachments == [
        {
            "id": user_text_attachment.id,
            "uploader_id": user_text_attachment.uploader_id,
            "uploader_name": user_text_attachment.uploader_name,
            "uploader_slug": user_text_attachment.uploader_slug,
            "uploaded_at": attachment_uploaded_at.isoformat(),
            "name": user_text_attachment.name,
            "slug": user_text_attachment.slug,
            "filetype_id": user_text_attachment.filetype_id,
            "dimensions": None,
            "thumbnail": None,
            "size": user_text_attachment.size,
            "change": "+",
        },
    ]
    assert post_edit.added_attachments == 1
    assert post_edit.removed_attachments == 0


def test_private_thread_edit_view_adds_attachment_to_deleted_list(
    user_client, user_private_thread, user_text_attachment
):
    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            PostForm.delete_attachment_field: str(user_text_attachment.id),
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, user_private_thread.title)
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
    "action_name", (Formset.preview_action, PostForm.upload_action)
)
def test_private_thread_edit_view_maintains_deleted_attachments_list(
    action_name, user_client, user_private_thread, user_text_attachment
):
    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
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
    assert_contains(response, user_private_thread.title)
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


def test_private_thread_edit_view_deletes_attachment_on_submit(
    user_client, user_private_thread, user_text_attachment
):
    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            PostForm.deleted_attachment_ids_field: [str(user_text_attachment.id)],
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert response.status_code == 302

    user_private_thread.refresh_from_db()
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )

    user_text_attachment.refresh_from_db()
    assert user_text_attachment.category_id is None
    assert user_text_attachment.thread_id is None
    assert user_text_attachment.post_id is None
    assert user_text_attachment.is_deleted

    post_edit = PostEdit.objects.get(post=user_private_thread.first_post.id)
    assert post_edit.attachments == []
    assert post_edit.added_attachments == 0
    assert post_edit.removed_attachments == 0


def test_private_thread_edit_view_displays_associated_attachment(
    user_client, user_private_thread, text_attachment
):
    text_attachment.associate_with_post(user_private_thread.first_post)
    text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, user_private_thread.title)
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
def test_private_thread_edit_view_displays_associated_attachment_if_uploads_are_disabled(
    user_client, user_private_thread, text_attachment
):
    text_attachment.associate_with_post(user_private_thread.first_post)
    text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, user_private_thread.title)
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


def test_private_thread_edit_view_displays_associated_attachment_for_user_without_upload_permission(
    members_group, user_client, user_private_thread, text_attachment
):
    members_group.can_upload_attachments = CanUploadAttachments.THREADS
    members_group.save()

    text_attachment.associate_with_post(user_private_thread.first_post)
    text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, user_private_thread.title)
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


def test_private_thread_edit_view_adds_existing_attachment_to_deleted_list(
    user_client, user_private_thread, text_attachment
):
    text_attachment.associate_with_post(user_private_thread.first_post)
    text_attachment.save()

    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            PostForm.attachment_ids_field: [str(text_attachment.id)],
            PostForm.delete_attachment_field: str(text_attachment.id),
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, user_private_thread.title)
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
def test_private_thread_edit_view_adds_existing_attachment_to_deleted_list_if_uploads_are_disabled(
    user_client, user_private_thread, text_attachment
):
    text_attachment.associate_with_post(user_private_thread.first_post)
    text_attachment.save()

    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            PostForm.attachment_ids_field: [str(text_attachment.id)],
            PostForm.delete_attachment_field: str(text_attachment.id),
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, user_private_thread.title)
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


def test_private_thread_edit_view_adds_existing_attachment_to_deleted_list_for_user_without_upload_permission(
    members_group, user_client, user_private_thread, text_attachment
):
    members_group.can_upload_attachments = CanUploadAttachments.THREADS
    members_group.save()

    text_attachment.associate_with_post(user_private_thread.first_post)
    text_attachment.save()

    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            PostForm.attachment_ids_field: [str(text_attachment.id)],
            PostForm.delete_attachment_field: str(text_attachment.id),
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, user_private_thread.title)
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


def test_private_thread_edit_view_deletes_existing_attachment_on_submit(
    user_client, user_private_thread, text_attachment
):
    text_attachment.associate_with_post(user_private_thread.first_post)
    text_attachment.save()

    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            PostForm.attachment_ids_field: [str(text_attachment.id)],
            PostForm.deleted_attachment_ids_field: [str(text_attachment.id)],
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert response.status_code == 302

    user_private_thread.refresh_from_db()
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )

    text_attachment.refresh_from_db()
    assert text_attachment.category_id is None
    assert text_attachment.thread_id is None
    assert text_attachment.post_id is None
    assert text_attachment.is_deleted

    post_edit = PostEdit.objects.get(post=user_private_thread.first_post)
    assert post_edit.attachments == [
        {
            "id": text_attachment.id,
            "uploader_id": text_attachment.uploader_id,
            "uploader_name": text_attachment.uploader_name,
            "uploader_slug": text_attachment.uploader_slug,
            "uploaded_at": text_attachment.uploaded_at.isoformat(),
            "name": text_attachment.name,
            "slug": text_attachment.slug,
            "filetype_id": text_attachment.filetype_id,
            "dimensions": None,
            "thumbnail": None,
            "size": text_attachment.size,
            "change": "-",
        },
    ]
    assert post_edit.added_attachments == 0
    assert post_edit.removed_attachments == 1


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE.value)
def test_private_thread_edit_view_deletes_existing_attachment_on_submit_if_uploads_are_disabled(
    user_client, user_private_thread, text_attachment
):
    text_attachment.associate_with_post(user_private_thread.first_post)
    text_attachment.save()

    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            PostForm.attachment_ids_field: [str(text_attachment.id)],
            PostForm.deleted_attachment_ids_field: [str(text_attachment.id)],
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert response.status_code == 302

    user_private_thread.refresh_from_db()
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )

    text_attachment.refresh_from_db()
    assert text_attachment.category_id is None
    assert text_attachment.thread_id is None
    assert text_attachment.post_id is None
    assert text_attachment.is_deleted


def test_private_thread_edit_view_deletes_existing_attachment_on_submit_for_user_without_upload_permission(
    members_group, user_client, user_private_thread, text_attachment
):
    members_group.can_upload_attachments = CanUploadAttachments.THREADS
    members_group.save()

    text_attachment.associate_with_post(user_private_thread.first_post)
    text_attachment.save()

    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            PostForm.attachment_ids_field: [str(text_attachment.id)],
            PostForm.deleted_attachment_ids_field: [str(text_attachment.id)],
            "posting-title-title": "Edited title",
            "posting-post-post": "Edited post",
        },
    )
    assert response.status_code == 302

    user_private_thread.refresh_from_db()
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )

    text_attachment.refresh_from_db()
    assert text_attachment.category_id is None
    assert text_attachment.thread_id is None
    assert text_attachment.post_id is None
    assert text_attachment.is_deleted


def test_private_thread_edit_view_embeds_attachments_in_preview(
    user_client, user_private_thread, user_image_attachment
):
    response = user_client.post(
        reverse(
            "misago:private-thread-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            Formset.preview_action: "true",
            PostForm.attachment_ids_field: [str(user_image_attachment.id)],
            "posting-title-title": "Edited title",
            "posting-post-post": (
                f"Edit: <attachment={user_image_attachment.name}:{user_image_attachment.id}>"
            ),
        },
    )
    assert_contains(response, "Edit thread")
    assert_contains(response, user_private_thread.title)
    assert_contains(response, "Message preview")
    assert_contains_element(response, "a", href=user_image_attachment.get_details_url())
    assert_contains_element(
        response, "img", src=user_image_attachment.get_absolute_url()
    )


def test_private_thread_edit_view_shows_error_404_if_thread_is_accessed(
    user_client, thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-edit",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
    )
    assert_not_contains(response, "Edit thread", status_code=404)
    assert_not_contains(response, thread.title, status_code=404)
