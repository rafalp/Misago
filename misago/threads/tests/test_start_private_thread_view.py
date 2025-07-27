import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from ...attachments.enums import AllowedAttachments
from ...attachments.models import Attachment
from ...conf.test import override_dynamic_settings
from ...permissions.enums import CanUploadAttachments
from ...posting.forms import PostForm
from ...posting.formsets import PostingFormset
from ...test import (
    assert_contains,
    assert_contains_element,
    assert_not_contains,
)
from ..models import Thread


def test_start_private_thread_view_displays_login_page_to_guests(db, client):
    response = client.get(reverse("misago:start-private-thread"))
    assert_contains(response, "Sign in to start new thread")


def test_start_private_thread_view_displays_error_page_to_users_without_private_threads_permission(
    user, user_client
):
    user.group.can_use_private_threads = False
    user.group.save()

    response = user_client.get(reverse("misago:start-private-thread"))
    assert_contains(
        response,
        "You can&#x27;t use private threads.",
        status_code=403,
    )


def test_start_private_thread_view_displays_error_page_to_users_without_start_threads_permission(
    user, user_client
):
    user.group.can_start_private_threads = False
    user.group.save()

    response = user_client.get(reverse("misago:start-private-thread"))
    assert_contains(
        response,
        "You can&#x27;t start new private threads.",
        status_code=403,
    )


def test_start_private_thread_view_displays_form_page_to_users(user_client):
    response = user_client.get(reverse("misago:start-private-thread"))
    assert_contains(response, "Start new private thread")


def test_start_private_thread_view_posts_new_thread(
    user_client, user, admin, moderator, other_user
):
    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            "posting-invite-users-users": [
                admin.username,
                moderator.username,
                other_user.username,
            ],
            "posting-invite-users-users_noscript": "",
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert response.status_code == 302

    thread = Thread.objects.get(slug="hello-world")
    assert response["location"] == reverse(
        "misago:private-thread", kwargs={"id": thread.id, "slug": thread.slug}
    )

    assert len(thread.private_thread_member_ids) == 4
    assert thread.private_thread_owner_id == user.id
    assert user.id in thread.private_thread_member_ids
    assert admin.id in thread.private_thread_member_ids
    assert moderator.id in thread.private_thread_member_ids
    assert other_user.id in thread.private_thread_member_ids


def test_start_private_thread_view_posts_new_thread_using_noscript_fallback(
    user_client, user, admin, moderator, other_user
):
    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            "posting-invite-users-users": [],
            "posting-invite-users-users_noscript": (
                f"{admin.username},{moderator.username} {other_user.username}"
            ),
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert response.status_code == 302

    thread = Thread.objects.get(slug="hello-world")
    assert response["location"] == reverse(
        "misago:private-thread", kwargs={"id": thread.id, "slug": thread.slug}
    )

    assert len(thread.private_thread_member_ids) == 4
    assert thread.private_thread_owner_id == user.id
    assert user.id in thread.private_thread_member_ids
    assert admin.id in thread.private_thread_member_ids
    assert moderator.id in thread.private_thread_member_ids
    assert other_user.id in thread.private_thread_member_ids


def test_start_private_thread_view_previews_message(user_client, other_user):
    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            PostingFormset.preview_action: "true",
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert_contains(response, "Start new private thread")
    assert_contains(response, "Message preview")


def test_start_private_thread_view_keeps_invited_users_field_value(
    user_client, other_user
):
    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            PostingFormset.preview_action: "true",
            "posting-invite-users-users": [other_user.username],
            "posting-invite-users-users_noscript": "",
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert_contains(response, "Start new private thread")
    assert_contains(response, "Message preview")
    assert_contains(response, other_user.username)


def test_start_private_thread_view_validates_invited_users(user_client, user):
    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            "posting-invite-users-users": [user.username],
            "posting-invite-users-users_noscript": "",
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert_contains(response, "Start new private thread")
    assert_contains(response, "You can&#x27;t invite yourself.")


def test_start_private_thread_view_ignores_user_inviting_self_if_other_users_are_invited(
    user_client, user, other_user, admin, moderator
):
    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            "posting-invite-users-users": [user.username, other_user.username],
            "posting-invite-users-users_noscript": "",
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert response.status_code == 302

    thread = Thread.objects.get(slug="hello-world")
    assert response["location"] == reverse(
        "misago:private-thread", kwargs={"id": thread.id, "slug": thread.slug}
    )

    assert len(thread.private_thread_member_ids) == 2
    assert user.id in thread.private_thread_member_ids
    assert other_user.id in thread.private_thread_member_ids


def test_start_private_thread_view_validates_thread_title(user_client, other_user):
    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            "posting-invite-users-users": [other_user.username],
            "posting-invite-users-users_noscript": "",
            "posting-title-title": "????",
            "posting-post-post": "How's going?",
        },
    )
    assert_contains(response, "Start new private thread")
    assert_contains(response, "Thread title must include alphanumeric characters.")


def test_start_private_thread_view_validates_post(user_client, other_user):
    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            "posting-invite-users-users": [other_user.username],
            "posting-invite-users-users_noscript": "",
            "posting-title-title": "Hello world",
            "posting-post-post": "?",
        },
    )
    assert_contains(response, "Start new private thread")
    assert_contains(
        response, "Posted message must be at least 5 characters long (it has 1)."
    )


def test_start_private_thread_view_validates_posted_contents(
    user_client, other_user, posted_contents_validator
):
    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            "posting-invite-users-users": [other_user.username],
            "posting-invite-users-users_noscript": "",
            "posting-title-title": "Hello world",
            "posting-post-post": "This is a spam message",
        },
    )
    assert_contains(response, "Start new private thread")
    assert_contains(response, "Your message contains spam!")


def test_start_private_thread_view_runs_flood_control(
    user_client, other_user, user_reply
):
    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            "posting-invite-users-users": [other_user.username],
            "posting-invite-users-users_noscript": "",
            "posting-title-title": "Hello world",
            "posting-post-post": "This is a flood message",
        },
    )
    assert_contains(response, "Start new private thread")
    assert_contains(
        response, "You can&#x27;t post a new message so soon after the previous one."
    )


def test_start_private_thread_view_displays_attachments_form(user_client):
    response = user_client.get(reverse("misago:start-private-thread"))
    assert_contains(response, "Start new private thread")
    assert_contains(response, "misago-editor-attachments=")


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE.value)
def test_start_private_thread_view_hides_attachments_form_if_uploads_are_disabled(
    user_client, default_category
):
    response = user_client.get(reverse("misago:start-private-thread"))
    assert_contains(response, "Start new private thread")
    assert_not_contains(response, "misago-editor-attachments=")


def test_start_private_thread_view_hides_attachments_form_if_user_has_no_group_permission(
    members_group, user_client
):
    members_group.can_upload_attachments = CanUploadAttachments.THREADS
    members_group.save()

    response = user_client.get(reverse("misago:start-private-thread"))
    assert_contains(response, "Start new private thread")
    assert_not_contains(response, "misago-editor-attachments=")


def test_start_private_thread_view_uploads_attachment_on_submit(
    user, user_client, other_user, teardown_attachments
):
    assert not Attachment.objects.exists()

    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            "posting-invite-users-users": [other_user.username],
            "posting-invite-users-users_noscript": "",
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
            "posting-post-upload": [
                SimpleUploadedFile("test.txt", b"Hello world!", "text/plain"),
            ],
        },
    )
    assert response.status_code == 302

    thread = Thread.objects.get(slug="hello-world")
    assert response["location"] == reverse(
        "misago:private-thread", kwargs={"id": thread.pk, "slug": thread.slug}
    )

    attachment = Attachment.objects.get(uploader=user)
    assert attachment.category_id == thread.category_id
    assert attachment.thread_id == thread.id
    assert attachment.post_id == thread.first_post_id
    assert attachment.uploader_id == user.id
    assert not attachment.is_deleted
    assert attachment.name == "test.txt"


@pytest.mark.parametrize(
    "action_name", (PostingFormset.preview_action, PostForm.upload_action)
)
def test_start_private_thread_view_uploads_attachment_on_preview_or_upload(
    action_name, user, user_client, other_user, teardown_attachments
):
    assert not Attachment.objects.exists()

    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            action_name: "true",
            "posting-invite-users-users": [other_user.username],
            "posting-invite-users-users_noscript": "",
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
            "posting-post-upload": [
                SimpleUploadedFile("test.txt", b"Hello world!", "text/plain"),
            ],
        },
    )
    assert_contains(response, "Start new private thread")
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
def test_start_private_thread_view_displays_image_attachment(
    action_name, user_client, other_user, user_image_attachment
):
    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_image_attachment.id)],
            "posting-invite-users-users": [other_user.username],
            "posting-invite-users-users_noscript": "",
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert_contains(response, "Start new private thread")
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
def test_start_private_thread_view_displays_image_with_thumbnail_attachment(
    action_name, user_client, other_user, user_image_thumbnail_attachment
):
    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_image_thumbnail_attachment.id)],
            "posting-invite-users-users": [other_user.username],
            "posting-invite-users-users_noscript": "",
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert_contains(response, "Start new private thread")
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
def test_start_private_thread_view_displays_video_attachment(
    action_name, user_client, other_user, user_video_attachment
):
    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_video_attachment.id)],
            "posting-invite-users-users": [other_user.username],
            "posting-invite-users-users_noscript": "",
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert_contains(response, "Start new private thread")
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
def test_start_private_thread_view_displays_file_attachment(
    action_name, user_client, other_user, user_text_attachment
):
    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            "posting-invite-users-users": [other_user.username],
            "posting-invite-users-users_noscript": "",
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert_contains(response, "Start new private thread")
    assert_contains(response, "misago-editor-attachments=")

    assert_contains(response, user_text_attachment.name)
    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.attachment_ids_field,
        value=user_text_attachment.id,
    )


def test_start_private_thread_view_associates_unused_attachment_on_submit(
    user_client, other_user, user_text_attachment
):
    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            "posting-invite-users-users": [other_user.username],
            "posting-invite-users-users_noscript": "",
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert response.status_code == 302

    thread = Thread.objects.get(slug="hello-world")
    assert response["location"] == reverse(
        "misago:private-thread", kwargs={"id": thread.pk, "slug": thread.slug}
    )

    user_text_attachment.refresh_from_db()
    assert user_text_attachment.category_id == thread.category_id
    assert user_text_attachment.thread_id == thread.id
    assert user_text_attachment.post_id == thread.first_post_id
    assert not user_text_attachment.is_deleted


def test_start_private_thread_view_adds_attachment_to_deleted_list(
    user_client, other_user, user_text_attachment
):
    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            PostForm.delete_attachment_field: str(user_text_attachment.id),
            "posting-invite-users-users": [other_user.username],
            "posting-invite-users-users_noscript": "",
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert_contains(response, "Start new private thread")
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
def test_start_private_thread_view_maintains_deleted_attachments_list(
    action_name, user_client, other_user, user_text_attachment
):
    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            PostForm.deleted_attachment_ids_field: [str(user_text_attachment.id)],
            "posting-invite-users-users": [other_user.username],
            "posting-invite-users-users_noscript": "",
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert_contains(response, "Start new private thread")
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


def test_start_private_thread_view_deletes_attachment_on_submit(
    user_client, other_user, user_text_attachment
):
    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            PostForm.deleted_attachment_ids_field: [str(user_text_attachment.id)],
            "posting-invite-users-users": [other_user.username],
            "posting-invite-users-users_noscript": "",
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert response.status_code == 302

    thread = Thread.objects.get(slug="hello-world")
    assert response["location"] == reverse(
        "misago:private-thread", kwargs={"id": thread.pk, "slug": thread.slug}
    )

    user_text_attachment.refresh_from_db()
    assert user_text_attachment.category_id is None
    assert user_text_attachment.thread_id is None
    assert user_text_attachment.post_id is None
    assert user_text_attachment.is_deleted


def test_start_private_thread_view_embeds_attachments_in_preview(
    user_client, other_user, default_category, user_image_attachment
):
    response = user_client.post(
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        ),
        {
            PostingFormset.preview_action: "true",
            PostForm.attachment_ids_field: [str(user_image_attachment.id)],
            "posting-invite-users-users": [other_user.username],
            "posting-invite-users-users_noscript": "",
            "posting-title-title": "Hello world",
            "posting-post-post": (
                f"Attachment: <attachment={user_image_attachment.name}:{user_image_attachment.id}>"
            ),
        },
    )
    assert_contains(response, "Start new thread")
    assert_contains(response, "Message preview")
    assert_contains_element(response, "a", href=user_image_attachment.get_details_url())
    assert_contains_element(
        response, "img", src=user_image_attachment.get_absolute_url()
    )
