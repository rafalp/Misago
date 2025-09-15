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
from ..forms import PostForm
from ..formsets import Formset


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


def test_thread_post_edit_view_shows_error_404_if_thread_doesnt_exist(user_client):
    response = user_client.get(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": 100,
                "slug": "not-found",
                "post_id": 100,
            },
        )
    )
    assert response.status_code == 404


def test_thread_post_edit_view_shows_error_404_to_users_without_see_category_permission(
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


def test_thread_post_edit_view_shows_error_404_to_users_without_browse_category_permission(
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


def test_thread_post_edit_view_shows_error_404_to_users_who_cant_see_thread(
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


def test_thread_post_edit_view_shows_error_404_if_post_is_not_part_of_thread(
    thread_reply_factory, user_client, thread, other_thread
):
    post = thread_reply_factory(other_thread)

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


def test_thread_post_edit_view_shows_error_403_to_users_who_cant_edit_posts(
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


def test_thread_post_edit_view_shows_error_403_to_users_who_cant_edit_other_users_posts(
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


def test_thread_post_edit_view_shows_error_403_to_users_who_cant_edit_deleted_users_posts(
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


def test_thread_post_edit_view_shows_error_403_to_users_who_cant_see_post_contents(
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


def test_thread_post_edit_view_shows_error_403_to_users_without_closed_category_permission(
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


def test_thread_post_edit_view_shows_error_403_to_users_without_closed_thread_permission(
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


def test_thread_post_edit_view_shows_error_403_to_users_without_protected_post_permission(
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
    assert_contains(response, post.original)
    assert_contains(response, "Save")
    assert_contains(response, "?inline=true")


def test_thread_post_edit_view_updates_thread_post(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
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
            kwargs={"id": thread.id, "slug": thread.slug},
        )
        + f"#post-{post.id}"
    )

    post.refresh_from_db()
    assert post.original == "Edited"
    assert post.edits == 1


def test_thread_post_edit_view_updates_thread_post_in_htmx(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
        {
            "posting-post-post": "Edited",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 204

    assert (
        response["hx-redirect"]
        == reverse(
            "misago:thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
        + f"#post-{post.id}"
    )

    post.refresh_from_db()
    assert post.original == "Edited"
    assert post.edits == 1


def test_thread_post_edit_view_updates_thread_post_inline_in_htmx(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        )
        + "?inline=true",
        {
            "posting-post-post": "Edited",
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, "<p>Edited</p>")

    post.refresh_from_db()
    assert post.original == "Edited"
    assert post.edits == 1


def test_thread_post_edit_view_previews_message(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
        {
            Formset.preview_action: "true",
            "posting-post-post": "How is going?",
        },
    )
    assert_contains(response, "Edit post")
    assert_contains(response, "Message preview")
    assert_contains(response, thread.title)
    assert_contains(response, "<p>How is going?</p>")


def test_thread_post_edit_view_previews_message_in_htmx(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
        {
            Formset.preview_action: "true",
            "posting-post-post": "How is going?",
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Edit post")
    assert_contains(response, "Message preview")
    assert_contains(response, "<p>How is going?</p>")


def test_thread_post_edit_view_previews_message_inline_in_htmx(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
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


def test_thread_post_edit_view_validates_post(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
        {
            "posting-post-post": "?",
        },
    )
    assert_contains(response, "Edit post")
    assert_contains(response, thread.title)
    assert_contains(
        response, "Posted message must be at least 5 characters long (it has 1)."
    )


def test_thread_post_edit_view_validates_posted_contents(
    thread_reply_factory, user_client, user, thread, posted_contents_validator
):
    post = thread_reply_factory(thread, poster=user)

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
        {
            "posting-post-post": "This is a spam message",
        },
    )
    assert_contains(response, "Edit post")
    assert_contains(response, thread.title)
    assert_contains(response, "Your message contains spam!")


def test_thread_post_edit_view_skips_flood_control(
    thread_reply_factory, user_client, user, user_reply, thread
):
    post = thread_reply_factory(thread, poster=user)

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
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
            kwargs={"id": thread.id, "slug": thread.slug},
        )
        + f"#post-{post.id}"
    )

    post.refresh_from_db()

    assert post.original == "This is a flood message"
    assert post.edits == 1


def test_thread_post_edit_view_displays_attachments_form(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    response = user_client.get(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
    )
    assert_contains(response, "Edit post")
    assert_contains(response, "misago-editor-attachments=")


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE.value)
def test_thread_post_edit_view_hides_attachments_form_if_uploads_are_disabled(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    response = user_client.get(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
    )
    assert_contains(response, "Edit post")
    assert_not_contains(response, "misago-editor-attachments=")


def test_thread_post_edit_view_hides_attachments_form_if_user_has_no_group_permission(
    thread_reply_factory, members_group, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_upload_attachments = CanUploadAttachments.NEVER
    members_group.save()

    response = user_client.get(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
    )
    assert_contains(response, "Edit post")
    assert_not_contains(response, "misago-editor-attachments=")


def test_thread_post_edit_view_hides_attachments_form_if_user_has_no_category_permission(
    thread_reply_factory, members_group, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    CategoryGroupPermission.objects.filter(
        category=thread.category,
        group=members_group,
        permission=CategoryPermission.ATTACHMENTS,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
    )
    assert_contains(response, "Edit post")
    assert_contains(response, thread.title)
    assert_not_contains(response, "misago-editor-attachments=")


def test_thread_post_edit_view_uploads_attachment_on_submit(
    thread_reply_factory, user_client, user, thread, teardown_attachments
):
    post = thread_reply_factory(thread, poster=user)

    assert not Attachment.objects.exists()

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
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
    assert attachment.category_id == thread.category_id
    assert attachment.thread_id == thread.id
    assert attachment.post_id == post.id
    assert attachment.uploader_id == user.id
    assert not attachment.is_deleted
    assert attachment.name == "test.txt"


@pytest.mark.parametrize(
    "action_name", (Formset.preview_action, PostForm.upload_action)
)
def test_thread_post_edit_view_uploads_attachment_on_preview_or_upload(
    action_name, thread_reply_factory, user_client, user, thread, teardown_attachments
):
    post = thread_reply_factory(thread, poster=user)

    assert not Attachment.objects.exists()

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
        {
            action_name: "true",
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
def test_thread_post_edit_view_displays_image_attachment(
    action_name, thread_reply_factory, user_client, user, thread, user_image_attachment
):
    post = thread_reply_factory(thread, poster=user)

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_image_attachment.id)],
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit post")
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
def test_thread_post_edit_view_displays_image_with_thumbnail_attachment(
    action_name,
    thread_reply_factory,
    user_client,
    user,
    thread,
    user_image_thumbnail_attachment,
):
    post = thread_reply_factory(thread, poster=user)

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_image_thumbnail_attachment.id)],
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit post")
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
def test_thread_post_edit_view_displays_video_attachment(
    action_name, thread_reply_factory, user_client, user, thread, user_video_attachment
):
    post = thread_reply_factory(thread, poster=user)

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_video_attachment.id)],
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit post")
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
def test_thread_post_edit_view_displays_file_attachment(
    action_name, thread_reply_factory, user_client, user, thread, user_text_attachment
):
    post = thread_reply_factory(thread, poster=user)

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit post")
    assert_contains(response, "misago-editor-attachments=")

    assert_contains(response, user_text_attachment.name)
    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.attachment_ids_field,
        value=user_text_attachment.id,
    )


def test_thread_post_edit_view_associates_unused_attachment_on_submit(
    thread_reply_factory, user_client, user, thread, user_text_attachment
):
    post = thread_reply_factory(thread, poster=user)

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
        {
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            "posting-post-post": "Edited post",
        },
    )
    assert response.status_code == 302

    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"id": thread.pk, "slug": thread.slug},
        )
        + f"#post-{post.id}"
    )

    user_text_attachment.refresh_from_db()
    assert user_text_attachment.category_id == thread.category_id
    assert user_text_attachment.thread_id == thread.id
    assert user_text_attachment.post_id == post.id
    assert not user_text_attachment.is_deleted


def test_thread_post_edit_view_adds_attachment_to_deleted_list(
    thread_reply_factory, user_client, user, thread, user_text_attachment
):
    post = thread_reply_factory(thread, poster=user)

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
        {
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            PostForm.delete_attachment_field: str(user_text_attachment.id),
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit post")
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
def test_thread_post_edit_view_maintains_deleted_attachments_list(
    action_name, thread_reply_factory, user_client, user, thread, user_text_attachment
):
    post = thread_reply_factory(thread, poster=user)

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            PostForm.deleted_attachment_ids_field: [str(user_text_attachment.id)],
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit post")
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


def test_thread_post_edit_view_deletes_attachment_on_submit(
    thread_reply_factory, user_client, user, thread, user_text_attachment
):
    post = thread_reply_factory(thread, poster=user)

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
        {
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            PostForm.deleted_attachment_ids_field: [str(user_text_attachment.id)],
            "posting-post-post": "Edited post",
        },
    )
    assert response.status_code == 302

    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
        + f"#post-{post.id}"
    )

    user_text_attachment.refresh_from_db()
    assert user_text_attachment.category_id is None
    assert user_text_attachment.thread_id is None
    assert user_text_attachment.post_id is None
    assert user_text_attachment.is_deleted


def test_thread_post_edit_view_displays_associated_attachment(
    thread_reply_factory, user_client, user, thread, text_attachment
):
    post = thread_reply_factory(thread, poster=user)

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
    )
    assert_contains(response, "Edit post")
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
def test_thread_post_edit_view_displays_associated_attachment_if_uploads_are_disabled(
    thread_reply_factory, user_client, user, thread, text_attachment
):
    post = thread_reply_factory(thread, poster=user)

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
    )
    assert_contains(response, "Edit post")
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


def test_thread_post_edit_view_displays_associated_attachment_for_user_without_upload_permission(
    thread_reply_factory, user_client, user, members_group, thread, text_attachment
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_upload_attachments = CanUploadAttachments.NEVER
    members_group.save()

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
    )
    assert_contains(response, "Edit post")
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


def test_thread_post_edit_view_displays_associated_attachment_for_user_without_category_permission(
    thread_reply_factory, user_client, user, members_group, thread, text_attachment
):
    post = thread_reply_factory(thread, poster=user)

    CategoryGroupPermission.objects.filter(
        category=thread.category,
        group=members_group,
        permission=CategoryPermission.ATTACHMENTS,
    ).delete()

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
    )
    assert_contains(response, "Edit post")
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


def test_thread_post_edit_view_adds_existing_attachment_to_deleted_list(
    thread_reply_factory, user_client, user, thread, text_attachment
):
    post = thread_reply_factory(thread, poster=user)

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
        {
            PostForm.attachment_ids_field: [str(text_attachment.id)],
            PostForm.delete_attachment_field: str(text_attachment.id),
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit post")
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
def test_thread_post_edit_view_adds_existing_attachment_to_deleted_list_if_uploads_are_disabled(
    thread_reply_factory, user_client, user, thread, text_attachment
):
    post = thread_reply_factory(thread, poster=user)

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
        {
            PostForm.attachment_ids_field: [str(text_attachment.id)],
            PostForm.delete_attachment_field: str(text_attachment.id),
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit post")
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


def test_thread_post_edit_view_adds_existing_attachment_to_deleted_list_for_user_without_upload_permission(
    thread_reply_factory, user_client, user, members_group, thread, text_attachment
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_upload_attachments = CanUploadAttachments.NEVER
    members_group.save()

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
        {
            PostForm.attachment_ids_field: [str(text_attachment.id)],
            PostForm.delete_attachment_field: str(text_attachment.id),
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit post")
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


def test_thread_post_edit_view_adds_existing_attachment_to_deleted_list_for_user_without_category_permission(
    thread_reply_factory, user_client, user, members_group, thread, text_attachment
):
    post = thread_reply_factory(thread, poster=user)

    CategoryGroupPermission.objects.filter(
        category=thread.category,
        group=members_group,
        permission=CategoryPermission.ATTACHMENTS,
    ).delete()

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
        {
            PostForm.attachment_ids_field: [str(text_attachment.id)],
            PostForm.delete_attachment_field: str(text_attachment.id),
            "posting-post-post": "Edited post",
        },
    )
    assert_contains(response, "Edit post")
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


def test_thread_post_edit_view_deletes_existing_attachment_on_submit(
    thread_reply_factory, user_client, user, thread, text_attachment
):
    post = thread_reply_factory(thread, poster=user)

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
        {
            PostForm.attachment_ids_field: [str(text_attachment.id)],
            PostForm.deleted_attachment_ids_field: [str(text_attachment.id)],
            "posting-post-post": "Edited post",
        },
    )
    assert response.status_code == 302

    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
        + f"#post-{post.id}"
    )

    text_attachment.refresh_from_db()
    assert text_attachment.category_id is None
    assert text_attachment.thread_id is None
    assert text_attachment.post_id is None
    assert text_attachment.is_deleted


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE.value)
def test_thread_post_edit_view_deletes_existing_attachment_on_submit_if_uploads_are_disabled(
    thread_reply_factory, user_client, user, thread, text_attachment
):
    post = thread_reply_factory(thread, poster=user)

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
        {
            PostForm.attachment_ids_field: [str(text_attachment.id)],
            PostForm.deleted_attachment_ids_field: [str(text_attachment.id)],
            "posting-post-post": "Edited post",
        },
    )
    assert response.status_code == 302

    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
        + f"#post-{post.id}"
    )

    text_attachment.refresh_from_db()
    assert text_attachment.category_id is None
    assert text_attachment.thread_id is None
    assert text_attachment.post_id is None
    assert text_attachment.is_deleted


def test_thread_post_edit_view_deletes_existing_attachment_on_submit_for_user_without_upload_permission(
    thread_reply_factory, user_client, user, members_group, thread, text_attachment
):
    post = thread_reply_factory(thread, poster=user)

    members_group.can_upload_attachments = CanUploadAttachments.NEVER
    members_group.save()

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
        {
            PostForm.attachment_ids_field: [str(text_attachment.id)],
            PostForm.deleted_attachment_ids_field: [str(text_attachment.id)],
            "posting-post-post": "Edited post",
        },
    )
    assert response.status_code == 302

    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
        + f"#post-{post.id}"
    )

    text_attachment.refresh_from_db()
    assert text_attachment.category_id is None
    assert text_attachment.thread_id is None
    assert text_attachment.post_id is None
    assert text_attachment.is_deleted


def test_thread_post_edit_view_deletes_existing_attachment_on_submit_for_user_without_category_permission(
    thread_reply_factory, user_client, user, members_group, thread, text_attachment
):
    post = thread_reply_factory(thread, poster=user)

    CategoryGroupPermission.objects.filter(
        category=thread.category,
        group=members_group,
        permission=CategoryPermission.ATTACHMENTS,
    ).delete()

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
        {
            PostForm.attachment_ids_field: [str(text_attachment.id)],
            PostForm.deleted_attachment_ids_field: [str(text_attachment.id)],
            "posting-post-post": "Edited post",
        },
    )
    assert response.status_code == 302

    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
        + f"#post-{post.id}"
    )

    text_attachment.refresh_from_db()
    assert text_attachment.category_id is None
    assert text_attachment.thread_id is None
    assert text_attachment.post_id is None
    assert text_attachment.is_deleted


def test_thread_post_edit_view_embeds_attachments_in_preview(
    thread_reply_factory, user_client, user, thread, user_image_attachment
):
    post = thread_reply_factory(thread, poster=user)

    response = user_client.post(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
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
    assert_contains(response, "Edit post")
    assert_contains(response, "Message preview")
    assert_contains_element(response, "a", href=user_image_attachment.get_details_url())
    assert_contains_element(
        response, "img", src=user_image_attachment.get_absolute_url()
    )


def test_thread_post_edit_view_shows_error_404_if_private_thread_post_is_accessed(
    thread_reply_factory, user_client, user_private_thread
):
    post = thread_reply_factory(user_private_thread)

    response = user_client.get(
        reverse(
            "misago:thread-post-edit",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert_not_contains(response, "Edit Post", status_code=404)
    assert_not_contains(response, user_private_thread.title, status_code=404)
