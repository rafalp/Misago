from unittest.mock import ANY

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from ...attachments.enums import AllowedAttachments
from ...attachments.models import Attachment
from ...conf.test import override_dynamic_settings
from ...permissions.enums import CanUploadAttachments, CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...polls.enums import PublicPollsAvailability
from ...polls.models import Poll
from ...test import assert_contains, assert_contains_element, assert_not_contains
from ...threads.models import Thread
from ..forms import PostForm
from ..formsets import Formset


def test_thread_start_view_displays_login_required_page_to_anonymous_user(
    client, default_category
):
    response = client.get(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_contains(response, "Sign in to start new thread", status_code=401)


def test_thread_start_view_shows_error_404_if_category_doesnt_exist(
    user_client, default_category
):
    response = user_client.get(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id * 100, "slug": "not-found"},
        )
    )
    assert response.status_code == 404


def test_thread_start_view_shows_error_404_to_users_without_see_category_permission(
    user_client, user, default_category
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.SEE,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        )
    )
    assert response.status_code == 404


def test_thread_start_view_shows_error_403_to_users_without_browse_category_permission(
    user_client, user, default_category
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.BROWSE,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_contains(
        response,
        "You can&#x27;t browse the contents of this category.",
        status_code=403,
    )


def test_thread_start_view_shows_error_403_to_users_without_start_threads_permission(
    user_client, user, default_category
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.START,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_contains(
        response,
        "You can&#x27;t start new threads in this category.",
        status_code=403,
    )


def test_thread_start_view_shows_error_403_to_users_without_post_in_closed_category_permission(
    user_client, default_category
):
    default_category.is_closed = True
    default_category.save()

    response = user_client.get(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_contains(
        response,
        "This category is closed.",
        status_code=403,
    )


def test_thread_start_view_displays_posting_form(user_client, default_category):
    response = user_client.get(
        reverse(
            "misago:thread-start",
            kwargs={
                "category_id": default_category.id,
                "slug": default_category.slug,
            },
        )
    )
    assert_contains(response, "Start thread")
    assert_contains(response, default_category.name)


def test_thread_start_view_displays_posting_form_to_users_with_permission_to_post_in_closed_category(
    user, user_client, default_category, members_group, moderators_group
):
    default_category.is_closed = True
    default_category.save()

    user.set_groups(members_group, [moderators_group])
    user.save()

    response = user_client.get(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_contains(response, "Start new thread")
    assert_contains(response, default_category.name)


def test_thread_start_view_posts_new_thread(user_client, default_category):
    response = user_client.post(
        reverse(
            "misago:thread-start",
            kwargs={
                "category_id": default_category.id,
                "slug": default_category.slug,
            },
        ),
        {
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert response.status_code == 302

    thread = Thread.objects.get(slug="hello-world")
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )


def test_thread_start_view_previews_new_thread(user_client, default_category):
    response = user_client.post(
        reverse(
            "misago:thread-start",
            kwargs={
                "category_id": default_category.id,
                "slug": default_category.slug,
            },
        ),
        {
            Formset.preview_action: "true",
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert_contains(response, "Start new thread")
    assert_contains(response, default_category.name)
    assert_contains(response, "Message preview")


def test_thread_start_view_validates_thread_title(user_client, default_category):
    response = user_client.post(
        reverse(
            "misago:thread-start",
            kwargs={
                "category_id": default_category.id,
                "slug": default_category.slug,
            },
        ),
        {
            "posting-title-title": "???",
            "posting-post-post": "How's going?",
        },
    )
    assert_contains(response, "Start new thread")
    assert_contains(response, default_category.name)
    assert_contains(response, "Thread title must include alphanumeric characters.")


def test_thread_start_view_validates_post(user_client, default_category):
    response = user_client.post(
        reverse(
            "misago:thread-start",
            kwargs={
                "category_id": default_category.id,
                "slug": default_category.slug,
            },
        ),
        {
            "posting-title-title": "Hello world",
            "posting-post-post": "?",
        },
    )
    assert_contains(response, "Start new thread")
    assert_contains(response, default_category.name)
    assert_contains(
        response, "Posted message must be at least 5 characters long (it has 1)."
    )


def test_thread_start_view_validates_posted_contents(
    user_client, default_category, posted_contents_validator
):
    response = user_client.post(
        reverse(
            "misago:thread-start",
            kwargs={
                "category_id": default_category.id,
                "slug": default_category.slug,
            },
        ),
        {
            "posting-title-title": "Hello world",
            "posting-post-post": "This is a spam message",
        },
    )
    assert_contains(response, "Start new thread")
    assert_contains(response, default_category.name)
    assert_contains(response, "Your message contains spam!")


def test_thread_start_view_runs_flood_control(
    user_client, default_category, user_reply
):
    response = user_client.post(
        reverse(
            "misago:thread-start",
            kwargs={
                "category_id": default_category.id,
                "slug": default_category.slug,
            },
        ),
        {
            "posting-title-title": "Hello world",
            "posting-post-post": "This is a flood message",
        },
    )
    assert_contains(response, "Start new thread")
    assert_contains(response, default_category.name)
    assert_contains(
        response, "You can&#x27;t post a new message so soon after the previous one."
    )


def test_thread_start_view_displays_attachments_form(user_client, default_category):
    response = user_client.get(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
    )
    assert_contains(response, "Start new thread")
    assert_contains(response, default_category.name)
    assert_contains(response, "misago-editor-attachments=")


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE.value)
def test_thread_start_view_hides_attachments_form_if_uploads_are_disabled(
    user_client, default_category
):
    response = user_client.get(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
    )
    assert_contains(response, "Start new thread")
    assert_contains(response, default_category.name)
    assert_not_contains(response, "misago-editor-attachments=")


def test_thread_start_view_hides_attachments_form_if_user_has_no_group_permission(
    members_group, user_client, default_category
):
    members_group.can_upload_attachments = CanUploadAttachments.NEVER
    members_group.save()

    response = user_client.get(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
    )
    assert_contains(response, "Start new thread")
    assert_contains(response, default_category.name)
    assert_not_contains(response, "misago-editor-attachments=")


def test_thread_start_view_hides_attachments_form_if_user_has_no_category_permission(
    members_group, user_client, default_category
):
    CategoryGroupPermission.objects.filter(
        category=default_category,
        group=members_group,
        permission=CategoryPermission.ATTACHMENTS,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
    )
    assert_contains(response, "Start new thread")
    assert_contains(response, default_category.name)
    assert_not_contains(response, "misago-editor-attachments=")


def test_thread_start_view_uploads_attachment_on_submit(
    user, user_client, default_category, teardown_attachments
):
    assert not Attachment.objects.exists()

    response = user_client.post(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
        {
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
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    attachment = Attachment.objects.get(uploader=user)
    assert attachment.category_id == thread.category_id
    assert attachment.thread_id == thread.id
    assert attachment.post_id == thread.first_post_id
    assert attachment.uploader_id == user.id
    assert not attachment.is_deleted
    assert attachment.name == "test.txt"


@pytest.mark.parametrize(
    "action_name", (Formset.preview_action, PostForm.upload_action)
)
def test_thread_start_view_uploads_attachment_on_preview_or_upload(
    action_name, user, user_client, default_category, teardown_attachments
):
    assert not Attachment.objects.exists()

    response = user_client.post(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
        {
            action_name: "true",
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
            "posting-post-upload": [
                SimpleUploadedFile("test.txt", b"Hello world!", "text/plain"),
            ],
        },
    )
    assert_contains(response, "Start new thread")
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
def test_thread_start_view_displays_image_attachment(
    action_name, user_client, default_category, user_image_attachment
):
    response = user_client.post(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_image_attachment.id)],
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert_contains(response, "Start new thread")
    assert_contains(response, default_category.name)
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
def test_thread_start_view_displays_image_with_thumbnail_attachment(
    action_name, user_client, default_category, user_image_thumbnail_attachment
):
    response = user_client.post(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_image_thumbnail_attachment.id)],
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert_contains(response, "Start new thread")
    assert_contains(response, default_category.name)
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
def test_thread_start_view_displays_video_attachment(
    action_name, user_client, default_category, user_video_attachment
):
    response = user_client.post(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_video_attachment.id)],
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert_contains(response, "Start new thread")
    assert_contains(response, default_category.name)
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
def test_thread_start_view_displays_file_attachment(
    action_name, user_client, default_category, user_text_attachment
):
    response = user_client.post(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert_contains(response, "Start new thread")
    assert_contains(response, default_category.name)
    assert_contains(response, "misago-editor-attachments=")

    assert_contains(response, user_text_attachment.name)
    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.attachment_ids_field,
        value=user_text_attachment.id,
    )


def test_start_view_associates_unused_attachment_on_submit(
    user_client, default_category, user_text_attachment
):
    response = user_client.post(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
        {
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert response.status_code == 302

    thread = Thread.objects.get(slug="hello-world")
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    user_text_attachment.refresh_from_db()
    assert user_text_attachment.category_id == thread.category_id
    assert user_text_attachment.thread_id == thread.id
    assert user_text_attachment.post_id == thread.first_post_id
    assert not user_text_attachment.is_deleted


def test_thread_start_view_adds_attachment_to_deleted_list(
    user_client, default_category, user_text_attachment
):
    response = user_client.post(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
        {
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            PostForm.delete_attachment_field: str(user_text_attachment.id),
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert_contains(response, "Start new thread")
    assert_contains(response, default_category.name)
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
def test_thread_start_view_maintains_deleted_attachments_list(
    action_name, user_client, default_category, user_text_attachment
):
    response = user_client.post(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            PostForm.deleted_attachment_ids_field: [str(user_text_attachment.id)],
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert_contains(response, "Start new thread")
    assert_contains(response, default_category.name)
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


def test_thread_start_view_deletes_attachment_on_submit(
    user_client, default_category, user_text_attachment
):
    response = user_client.post(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
        {
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            PostForm.deleted_attachment_ids_field: [str(user_text_attachment.id)],
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert response.status_code == 302

    thread = Thread.objects.get(slug="hello-world")
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    user_text_attachment.refresh_from_db()
    assert user_text_attachment.category_id is None
    assert user_text_attachment.thread_id is None
    assert user_text_attachment.post_id is None
    assert user_text_attachment.is_deleted


def test_thread_start_view_embeds_attachments_in_preview(
    user_client, default_category, user_image_attachment
):
    response = user_client.post(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
        {
            Formset.preview_action: "true",
            PostForm.attachment_ids_field: [str(user_image_attachment.id)],
            "posting-title-title": "Hello world",
            "posting-post-post": (
                f"Attachment: <attachment={user_image_attachment.name}:{user_image_attachment.id}>"
            ),
        },
    )
    assert_contains(response, "Start new thread")
    assert_contains(response, default_category.name)
    assert_contains(response, "Message preview")
    assert_contains_element(response, "a", href=user_image_attachment.get_details_url())
    assert_contains_element(
        response, "img", src=user_image_attachment.get_absolute_url()
    )


def test_thread_start_view_displays_poll_form(user_client, default_category):
    response = user_client.get(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
    )
    assert_contains(response, "Start new thread")
    assert_contains(response, default_category.name)
    assert_contains(response, "m-poll-choices-control")


def test_thread_start_view_hides_poll_form_for_user_without_permission(
    user_client, members_group, default_category
):
    members_group.can_start_polls = False
    members_group.save()

    response = user_client.get(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
    )
    assert_contains(response, "Start new thread")
    assert_contains(response, default_category.name)
    assert_not_contains(response, "m-poll-choices-control")


@override_dynamic_settings(enable_public_polls=PublicPollsAvailability.ENABLED)
def test_thread_start_view_displays_public_poll_option(user_client, default_category):
    response = user_client.get(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
    )
    assert_contains(response, "Start new thread")
    assert_contains(response, default_category.name)
    assert_contains(response, "is_public")


@override_dynamic_settings(enable_public_polls=PublicPollsAvailability.DISABLED)
def test_thread_start_view_hides_public_poll_option(user_client, default_category):
    response = user_client.get(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
    )
    assert_contains(response, "Start new thread")
    assert_contains(response, default_category.name)
    assert_not_contains(response, "is_public")


def test_thread_start_view_starts_thread_with_poll(user_client, user, default_category):
    response = user_client.post(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
        {
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
            "posting-poll-question": "What's your mood?",
            "posting-poll-choices_new": [
                "Great",
                "Okay",
                "About average",
                "Sad panda",
            ],
            "posting-poll-choices_new_noscript": "",
            "posting-poll-duration": "30",
            "posting-poll-max_choices": "2",
            "posting-poll-can_change_vote": "1",
            "posting-poll-is_public": "1",
        },
    )
    assert response.status_code == 302

    thread = Thread.objects.get(slug="hello-world")
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    assert thread.has_poll

    poll = Poll.objects.get(thread=thread)
    assert poll.category == default_category
    assert poll.thread == thread
    assert poll.starter == user
    assert poll.starter_name == user.username
    assert poll.starter_slug == user.slug
    assert poll.started_at
    assert poll.closed_at is None
    assert poll.question == "What's your mood?"
    assert poll.choices == [
        {
            "id": ANY,
            "name": "Great",
            "votes": 0,
        },
        {
            "id": ANY,
            "name": "Okay",
            "votes": 0,
        },
        {
            "id": ANY,
            "name": "About average",
            "votes": 0,
        },
        {
            "id": ANY,
            "name": "Sad panda",
            "votes": 0,
        },
    ]
    assert poll.duration == 30
    assert poll.max_choices == 2
    assert poll.can_change_vote
    assert poll.is_public
    assert not poll.is_closed
    assert poll.votes == 0
    assert poll.closed_by is None
    assert poll.closed_by_name is None
    assert poll.closed_by_slug is None

    choices_ids = [len(choice["id"]) for choice in poll.choices]
    assert choices_ids == [12, 12, 12, 12]


def test_thread_start_view_starts_thread_with_poll_form_disabled(
    user_client, members_group, default_category
):
    members_group.can_start_polls = False
    members_group.save()

    response = user_client.post(
        reverse(
            "misago:thread-start",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
        {
            "posting-title-title": "Hello world",
            "posting-post-post": "How's going?",
        },
    )
    assert response.status_code == 302

    thread = Thread.objects.get(slug="hello-world")
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )


def test_thread_start_view_shows_error_404_for_private_threads_category(
    user_client, private_threads_category
):
    response = user_client.get(
        reverse(
            "misago:thread-start",
            kwargs={
                "category_id": private_threads_category.id,
                "slug": private_threads_category.slug,
            },
        )
    )
    assert response.status_code == 404
