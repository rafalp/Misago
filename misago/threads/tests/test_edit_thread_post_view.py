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
from ...test import assert_contains, assert_not_contains
from ..test import reply_thread


def test_edit_thread_post_view_displays_login_page_to_guests(client, user_thread):
    response = client.get(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        )
    )
    assert_contains(response, "Sign in to edit posts")


def test_edit_thread_post_view_displays_error_page_to_user_who_cant_see_thread_category(
    user, user_client, user_thread
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.SEE,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        )
    )
    assert response.status_code == 404


def test_edit_thread_post_view_displays_error_page_to_user_who_cant_browse_thread_category(
    user, user_client, user_thread
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.BROWSE,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        )
    )
    assert response.status_code == 404


def test_edit_thread_post_view_displays_error_page_to_user_who_cant_edit_in_closed_category(
    user_client, user_thread
):
    user_thread.category.is_closed = True
    user_thread.category.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        )
    )

    assert_contains(
        response,
        "This category is closed.",
        status_code=403,
    )


def test_edit_thread_post_view_displays_error_page_to_user_who_cant_edit_in_closed_thread(
    user_client, user_thread
):
    user_thread.is_closed = True
    user_thread.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        )
    )

    assert_contains(
        response,
        "This thread is closed.",
        status_code=403,
    )


def test_edit_thread_post_view_displays_error_page_to_user_who_cant_edit_protected_post(
    user_client, user_thread
):
    post = user_thread.first_post
    post.is_protected = True
    post.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        )
    )

    assert_contains(
        response,
        "You can&#x27;t edit protected posts.",
        status_code=403,
    )


def test_edit_thread_post_view_displays_error_page_to_user_who_cant_edit_own_posts(
    user, user_client, user_thread
):
    user.group.can_edit_own_posts = False
    user.group.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        )
    )

    assert_contains(
        response,
        "You can&#x27;t edit posts.",
        status_code=403,
    )


def test_edit_thread_post_view_displays_error_page_to_user_trying_to_edit_other_user_post(
    user_client, user_thread, other_user
):
    post = reply_thread(user_thread, poster=other_user)

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug, "post": post.id},
        )
    )

    assert_contains(
        response,
        "You can&#x27;t edit other users posts.",
        status_code=403,
    )


def test_edit_thread_post_view_displays_edit_post_form(user_client, user_thread):
    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        )
    )
    assert_contains(response, "Edit post")
    assert_contains(response, user_thread.first_post.original)


def test_edit_thread_post_view_displays_inline_edit_post_form_in_htmx(
    user_client, user_thread
):
    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        )
        + "?inline=true",
        headers={"hx-request": "true"},
    )
    assert_contains(response, user_thread.first_post.original)
    assert_contains(response, "?inline=true")


def test_edit_thread_post_view_displays_edit_post_form_in_closed_category_to_moderator(
    user, user_client, user_thread, members_group, moderators_group
):
    user_thread.category.is_closed = True
    user_thread.category.save()

    user.set_groups(members_group, [moderators_group])
    user.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        )
    )

    assert_contains(response, "Edit post")
    assert_contains(response, user_thread.first_post.original)


def test_edit_thread_post_view_displays_edit_post_form_in_closed_thread_to_moderator(
    user, user_client, user_thread, members_group, moderators_group
):
    user_thread.is_closed = True
    user_thread.save()

    user.set_groups(members_group, [moderators_group])
    user.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        )
    )

    assert_contains(response, "Edit post")
    assert_contains(response, user_thread.first_post.original)


def test_edit_thread_post_view_displays_edit_post_form_for_protected_post_to_moderator(
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
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        )
    )

    assert_contains(response, "Edit post")
    assert_contains(response, user_thread.first_post.original)


def test_edit_thread_post_view_displays_edit_post_form_for_other_user_post_to_moderator(
    user, user_client, user_thread, other_user, members_group, moderators_group
):
    post = reply_thread(user_thread, poster=other_user)

    user.set_groups(members_group, [moderators_group])
    user.save()

    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={"id": user_thread.id, "slug": user_thread.slug, "post": post.id},
        )
    )

    assert_contains(response, "Edit post")
    assert_contains(response, post.original)


def test_edit_thread_post_view_updates_thread_post(user_client, user_thread):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        ),
        {
            "posting-post-post": "Edited",
        },
    )
    assert response.status_code == 302

    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"id": user_thread.pk, "slug": user_thread.slug},
        )
        + f"#post-{user_thread.first_post_id}"
    )

    post = user_thread.first_post
    post.refresh_from_db()

    assert post.original == "Edited"
    assert post.edits == 1


def test_edit_thread_post_view_updates_thread_post_in_htmx(user_client, user_thread):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        ),
        {
            "posting-post-post": "Edited",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 204

    user_thread.refresh_from_db()
    assert (
        response["hx-redirect"]
        == reverse(
            "misago:thread",
            kwargs={"id": user_thread.pk, "slug": user_thread.slug},
        )
        + f"#post-{user_thread.first_post_id}"
    )

    post = user_thread.first_post
    post.refresh_from_db()

    assert post.original == "Edited"
    assert post.edits == 1


def test_edit_thread_post_view_updates_thread_post_inline_in_htmx(
    user_client, user_thread
):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        )
        + "?inline=true",
        {
            "posting-post-post": "Edited",
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, "<p>Edited</p>")

    post = user_thread.first_post
    post.refresh_from_db()

    assert post.original == "Edited"
    assert post.edits == 1


def test_edit_thread_post_view_cancels_thread_post_edits_inline_in_htmx(
    user_client, user_thread
):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        )
        + "?inline=true",
        {
            "posting-post-post": "Edited",
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
                "post": user_thread.first_post_id,
            },
        ),
    )

    post = user_thread.first_post
    post.refresh_from_db()

    assert post.original == post_original
    assert post.edits == 0


def test_edit_thread_post_view_previews_message(user_client, user_thread):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        ),
        {
            PostingFormset.preview_action: "true",
            "posting-post-post": "How's going?",
        },
    )
    assert_contains(response, "Edit post")
    assert_contains(response, "Message preview")


def test_edit_thread_post_view_previews_message_in_htmx(user_client, user_thread):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        ),
        {
            PostingFormset.preview_action: "true",
            "posting-post-post": "How's going?",
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Edit post")
    assert_contains(response, "Message preview")


def test_edit_thread_post_view_previews_message_inline_in_htmx(
    user_client, user_thread
):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        )
        + "?inline=true",
        {
            PostingFormset.preview_action: "true",
            "posting-post-post": "How's going?",
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Message preview")
    assert_contains(response, "?inline=true")


def test_edit_thread_post_view_validates_post(user_client, user_thread):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        ),
        {
            "posting-post-post": "?",
        },
    )
    assert_contains(response, "Edit post")
    assert_contains(
        response, "Posted message must be at least 5 characters long (it has 1)."
    )


def test_edit_thread_post_view_validates_posted_contents(
    user_client, user_thread, posted_contents_validator
):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        ),
        {
            "posting-post-post": "This is a spam message",
        },
    )
    assert_contains(response, "Edit post")
    assert_contains(response, "Your message contains spam!")


def test_edit_thread_post_view_skips_flood_control(
    user_client, user_thread, user_reply
):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        ),
        {
            "posting-post-post": "This is a flood message",
        },
    )
    assert response.status_code == 302

    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"id": user_thread.pk, "slug": user_thread.slug},
        )
        + f"#post-{user_thread.first_post_id}"
    )

    post = user_thread.first_post
    post.refresh_from_db()

    assert post.original == "This is a flood message"
    assert post.edits == 1


def test_edit_thread_post_view_shows_error_if_private_thread_post_is_accessed(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post": user_private_thread.first_post_id,
            },
        ),
    )

    assert_not_contains(response, "Edit post", status_code=404)
    assert_not_contains(response, user_private_thread.title, status_code=404)


def test_edit_thread_post_view_displays_attachments_form(user_client, user_thread):
    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        ),
    )
    assert_contains(response, "Edit post")
    assert_contains(response, "misago-editor-attachments=")


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE.value)
def test_edit_thread_post_view_hides_attachments_form_if_uploads_are_disabled(
    user_client, user_thread
):
    response = user_client.get(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        ),
    )
    assert_contains(response, "Edit post")
    assert_not_contains(response, "misago-editor-attachments=")


def test_edit_thread_post_view_hides_attachments_form_if_user_has_no_group_permission(
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
                "post": user_thread.first_post_id,
            },
        ),
    )
    assert_contains(response, "Edit post")
    assert_not_contains(response, "misago-editor-attachments=")


def test_edit_thread_post_view_uploads_attachment_on_submit(
    user, user_client, user_thread, teardown_attachments
):
    assert not Attachment.objects.exists()

    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        ),
        {
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


def test_edit_thread_post_view_uploads_attachment_on_preview(
    user, user_client, user_thread, teardown_attachments
):
    assert not Attachment.objects.exists()

    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        ),
        {
            PostingFormset.preview_action: "true",
            "posting-post-post": "Edited post",
            "posting-post-upload": [
                SimpleUploadedFile("test.txt", b"Hello world!", "text/plain"),
            ],
        },
    )
    assert_contains(response, "Edit post")
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


def test_edit_thread_post_view_uploads_attachment_on_upload(
    user, user_client, user_thread, teardown_attachments
):
    assert not Attachment.objects.exists()

    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        ),
        {
            PostForm.upload_action: "true",
            "posting-post-post": "Edited post",
            "posting-post-upload": [
                SimpleUploadedFile("test.txt", b"Hello world!", "text/plain"),
            ],
        },
    )
    assert_contains(response, "Edit post")
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


@pytest.mark.parametrize(
    "action_name", (PostingFormset.preview_action, PostForm.upload_action)
)
def test_edit_thread_post_view_displays_image_attachment(
    action_name, user_client, user_thread, user_attachment
):
    user_attachment.name = "image-attachment.png"
    user_attachment.slug = "image-attachment-png"
    user_attachment.filetype_id = "png"
    user_attachment.upload = "attachments/image-attachment.png"
    user_attachment.dimensions = "200x200"
    user_attachment.save()

    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_attachment.id)],
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit post")
    assert_contains(response, "misago-editor-attachments=")

    assert_contains(response, user_attachment.name)
    assert_contains(response, user_attachment.get_absolute_url())
    assert_contains(response, f'value="{user_attachment.id}"')


@pytest.mark.parametrize(
    "action_name", (PostingFormset.preview_action, PostForm.upload_action)
)
def test_edit_thread_post_view_displays_image_with_thumbnail_attachment(
    action_name, user_client, user_thread, user_attachment
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
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_attachment.id)],
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit post")
    assert_contains(response, "misago-editor-attachments=")

    assert_contains(response, user_attachment.name)
    assert_contains(response, user_attachment.get_thumbnail_url())
    assert_contains(response, f'value="{user_attachment.id}"')


@pytest.mark.parametrize(
    "action_name", (PostingFormset.preview_action, PostForm.upload_action)
)
def test_edit_thread_post_view_displays_video_attachment(
    action_name, user_client, user_thread, user_attachment
):
    user_attachment.name = "video-attachment.mp4"
    user_attachment.slug = "video-attachment-mp4"
    user_attachment.filetype_id = "mp4"
    user_attachment.upload = "attachments/video-attachment.mp4"
    user_attachment.save()

    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_attachment.id)],
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit post")
    assert_contains(response, "misago-editor-attachments=")

    assert_contains(response, user_attachment.name)
    assert_contains(response, user_attachment.get_absolute_url())
    assert_contains(response, f'value="{user_attachment.id}"')


@pytest.mark.parametrize(
    "action_name", (PostingFormset.preview_action, PostForm.upload_action)
)
def test_edit_thread_post_view_displays_file_attachment(
    action_name, user_client, user_thread, user_attachment
):
    user_attachment.name = "document-attachment.pdf"
    user_attachment.slug = "document-attachment-pdf"
    user_attachment.filetype_id = "pdf"
    user_attachment.upload = "attachments/document-attachment.pdf"
    user_attachment.save()

    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_attachment.id)],
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit post")
    assert_contains(response, "misago-editor-attachments=")

    assert_contains(response, user_attachment.name)
    assert_contains(response, f'value="{user_attachment.id}"')


def test_edit_thread_post_view_associates_unused_attachment_on_submit(
    user_client, user_thread, user_attachment
):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        ),
        {
            PostForm.attachment_ids_field: [str(user_attachment.id)],
            "posting-post-post": "Edited post",
        },
    )
    assert response.status_code == 302

    assert (
        response["location"]
        == reverse(
            "misago:thread", kwargs={"id": user_thread.pk, "slug": user_thread.slug}
        )
        + f"#post-{user_thread.first_post_id}"
    )

    user_attachment.refresh_from_db()
    assert user_attachment.category_id == user_thread.category_id
    assert user_attachment.thread_id == user_thread.id
    assert user_attachment.post_id == user_thread.first_post_id
    assert not user_attachment.is_deleted


def test_edit_thread_post_view_adds_attachment_to_deleted_list(
    user_client, user_thread, user_attachment
):
    response = user_client.post(
        reverse(
            "misago:edit-thread",
            kwargs={
                "id": user_thread.id,
                "slug": user_thread.slug,
                "post": user_thread.first_post_id,
            },
        ),
        {
            PostForm.attachment_ids_field: [str(user_attachment.id)],
            PostForm.delete_attachment_field: str(user_attachment.id),
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit post")
    assert_contains(response, "misago-editor-attachments=")

    assert_contains(response, f'value="{user_attachment.id}"')
    assert_contains(response, f'name="{PostForm.deleted_attachment_ids_field}"')
    assert_not_contains(response, user_attachment.name)
    assert_not_contains(response, user_attachment.get_absolute_url())
