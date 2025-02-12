from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from ...attachments.enums import AllowedAttachments
from ...attachments.models import Attachment
from ...conf.test import override_dynamic_settings
from ...permissions.enums import CanUploadAttachments
from ...posting.forms import PostForm
from ...posting.formsets import PostingFormset
from ...test import assert_contains, assert_not_contains
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


def test_start_private_thread_view_posts_new_thread(user_client, other_user):
    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            "posting-invite-users-users": other_user.username,
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert response.status_code == 302

    thread = Thread.objects.get(slug="hello-world")
    assert response["location"] == reverse(
        "misago:private-thread", kwargs={"id": thread.id, "slug": thread.slug}
    )


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


def test_start_private_thread_view_validates_thread_title(user_client, other_user):
    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            "posting-invite-users-users": other_user.username,
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
            "posting-invite-users-users": other_user.username,
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
            "posting-invite-users-users": other_user.username,
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
            "posting-invite-users-users": other_user.username,
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
    user, other_user, user_client, teardown_attachments
):
    assert not Attachment.objects.exists()

    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            "posting-invite-users-users": other_user.username,
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


def test_start_private_thread_view_uploads_attachment_on_preview(
    user, other_user, user_client, teardown_attachments
):
    assert not Attachment.objects.exists()

    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            PostingFormset.preview_action: "true",
            "posting-invite-users-users": other_user.username,
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
    assert_contains(response, f'value="{attachment.id}"')


def test_start_private_thread_view_uploads_attachment_on_upload(
    user, other_user, user_client, teardown_attachments
):
    assert not Attachment.objects.exists()

    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            PostForm.upload_action: "true",
            "posting-invite-users-users": other_user.username,
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
    assert_contains(response, f'value="{attachment.id}"')


def test_start_private_thread_view_displays_image_attachment(
    other_user, user_client, user_attachment
):
    user_attachment.name = "image-attachment.png"
    user_attachment.slug = "image-attachment-png"
    user_attachment.filetype_id = "png"
    user_attachment.upload = "attachments/image-attachment.png"
    user_attachment.dimensions = "200x200"
    user_attachment.save()

    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            PostForm.upload_action: "true",
            PostForm.attachment_ids_field: [str(user_attachment.id)],
            "posting-invite-users-users": other_user.username,
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert_contains(response, "Start new private thread")
    assert_contains(response, "misago-editor-attachments=")

    assert_contains(response, user_attachment.name)
    assert_contains(response, user_attachment.get_absolute_url())
    assert_contains(response, f'value="{user_attachment.id}"')


def test_start_private_thread_view_displays_image_with_thumbnail_attachment(
    other_user, user_client, user_attachment
):
    user_attachment.name = "image-attachment.png"
    user_attachment.slug = "image-attachment-png"
    user_attachment.filetype_id = "png"
    user_attachment.upload = "attachments/image-attachment.png"
    user_attachment.dimensions = "200x200"
    user_attachment.thumbnail = "attachments/image-thumbnail.png"
    user_attachment.thumbnail_dimensions = "50x50"
    user_attachment.save()

    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            PostForm.upload_action: "true",
            PostForm.attachment_ids_field: [str(user_attachment.id)],
            "posting-invite-users-users": other_user.username,
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert_contains(response, "Start new private thread")
    assert_contains(response, "misago-editor-attachments=")

    assert_contains(response, user_attachment.name)
    assert_contains(response, user_attachment.get_thumbnail_url())
    assert_contains(response, f'value="{user_attachment.id}"')


def test_start_private_thread_view_displays_video_attachment(
    other_user, user_client, user_attachment
):
    user_attachment.name = "video-attachment.mp4"
    user_attachment.slug = "video-attachment-mp4"
    user_attachment.filetype_id = "mp4"
    user_attachment.upload = "attachments/video-attachment.mp4"
    user_attachment.save()

    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            PostForm.upload_action: "true",
            PostForm.attachment_ids_field: [str(user_attachment.id)],
            "posting-invite-users-users": other_user.username,
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert_contains(response, "Start new private thread")
    assert_contains(response, "misago-editor-attachments=")

    assert_contains(response, user_attachment.name)
    assert_contains(response, user_attachment.get_absolute_url())
    assert_contains(response, f'value="{user_attachment.id}"')


def test_start_private_thread_view_displays_file_attachment(
    other_user, user_client, user_attachment
):
    user_attachment.name = "document-attachment.pdf"
    user_attachment.slug = "document-attachment-pdf"
    user_attachment.filetype_id = "pdf"
    user_attachment.upload = "attachments/document-attachment.pdf"
    user_attachment.save()

    response = user_client.post(
        reverse("misago:start-private-thread"),
        {
            PostForm.upload_action: "true",
            PostForm.attachment_ids_field: [str(user_attachment.id)],
            "posting-invite-users-users": other_user.username,
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert_contains(response, "Start new private thread")
    assert_contains(response, "misago-editor-attachments=")

    assert_contains(response, user_attachment.name)
    assert_contains(response, f'value="{user_attachment.id}"')
