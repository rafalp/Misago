from unittest.mock import patch

from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...pagination.cursor import EmptyPageError
from ...test import assert_contains, assert_not_contains


def test_account_attachments_displays_login_page_for_guests(db, client):
    response = client.get(reverse("misago:account-attachments"))
    assert_contains(response, "Sign in to change your settings")


def test_account_attachments_shows_storage_for_user_without_attachments(user_client):
    response = user_client.get(reverse("misago:account-attachments"))
    assert response.status_code == 200


def test_account_attachments_shows_storage_for_user_with_used_attachment(
    user, user_client, attachment, post
):
    attachment.uploader = user
    attachment.category = post.category
    attachment.thread = post.thread
    attachment.post = post
    attachment.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert response.status_code == 200


def test_account_attachments_shows_storage_for_user_with_unused_attachment(
    user, user_client, attachment
):
    attachment.uploader = user
    attachment.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert response.status_code == 200


def test_account_attachments_shows_storage_for_user_with_used_and_unused_attachments(
    user, user_client, attachment, user_attachment, post
):
    attachment.uploader = user
    attachment.category = post.category
    attachment.thread = post.thread
    attachment.post = post
    attachment.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert response.status_code == 200


@override_dynamic_settings(unused_attachments_storage_limit=0)
def test_account_attachments_shows_storage_for_user_without_attachments_and_no_limits(
    members_group, user_client
):
    members_group.attachment_storage_limit = 0
    members_group.unused_attachments_storage_limit = 0
    members_group.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert response.status_code == 200


@override_dynamic_settings(unused_attachments_storage_limit=0)
def test_account_attachments_shows_storage_for_user_with_used_attachment_and_no_limits(
    user, members_group, user_client, attachment, post
):
    attachment.uploader = user
    attachment.category = post.category
    attachment.thread = post.thread
    attachment.post = post
    attachment.save()

    members_group.attachment_storage_limit = 0
    members_group.unused_attachments_storage_limit = 0
    members_group.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert response.status_code == 200


@override_dynamic_settings(unused_attachments_storage_limit=0)
def test_account_attachments_shows_storage_for_user_with_unused_attachment_and_no_limits(
    user, members_group, user_client, attachment
):
    attachment.uploader = user
    attachment.save()

    members_group.attachment_storage_limit = 0
    members_group.unused_attachments_storage_limit = 0
    members_group.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert response.status_code == 200


@override_dynamic_settings(unused_attachments_storage_limit=0)
def test_account_attachments_shows_storage_for_user_with_used_and_unused_attachments_and_no_limits(
    user, members_group, user_client, attachment, user_attachment, post
):
    attachment.uploader = user
    attachment.category = post.category
    attachment.thread = post.thread
    attachment.post = post
    attachment.save()

    members_group.attachment_storage_limit = 0
    members_group.unused_attachments_storage_limit = 0
    members_group.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert response.status_code == 200


def test_account_attachments_shows_storage_for_user_without_attachments_and_no_group_limits(
    members_group, user_client
):
    members_group.attachment_storage_limit = 0
    members_group.unused_attachments_storage_limit = 0
    members_group.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert response.status_code == 200


def test_account_attachments_shows_storage_for_user_with_used_attachment_and_no_group_limits(
    user, members_group, user_client, attachment, post
):
    attachment.uploader = user
    attachment.category = post.category
    attachment.thread = post.thread
    attachment.post = post
    attachment.save()

    members_group.attachment_storage_limit = 0
    members_group.unused_attachments_storage_limit = 0
    members_group.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert response.status_code == 200


def test_account_attachments_shows_storage_for_user_with_unused_attachment_and_no_group_limits(
    user, members_group, user_client, attachment
):
    attachment.uploader = user
    attachment.save()

    members_group.attachment_storage_limit = 0
    members_group.unused_attachments_storage_limit = 0
    members_group.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert response.status_code == 200


def test_account_attachments_shows_storage_for_user_with_used_and_unused_attachments_and_no_group_limits(
    user, members_group, user_client, attachment, user_attachment, post
):
    attachment.uploader = user
    attachment.category = post.category
    attachment.thread = post.thread
    attachment.post = post
    attachment.save()

    members_group.attachment_storage_limit = 0
    members_group.unused_attachments_storage_limit = 0
    members_group.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert response.status_code == 200


@override_dynamic_settings(unused_attachments_storage_limit=0)
def test_account_attachments_shows_storage_for_user_without_attachments_and_no_unused_limits(
    members_group, user_client
):
    members_group.unused_attachments_storage_limit = 0
    members_group.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert response.status_code == 200


@override_dynamic_settings(unused_attachments_storage_limit=0)
def test_account_attachments_shows_storage_for_user_with_used_attachment_and_no_unused_limits(
    user, members_group, user_client, attachment, post
):
    attachment.uploader = user
    attachment.category = post.category
    attachment.thread = post.thread
    attachment.post = post
    attachment.save()

    members_group.unused_attachments_storage_limit = 0
    members_group.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert response.status_code == 200


@override_dynamic_settings(unused_attachments_storage_limit=0)
def test_account_attachments_shows_storage_for_user_with_unused_attachment_and_no_unused_limits(
    user, members_group, user_client, attachment
):
    attachment.uploader = user
    attachment.save()

    members_group.unused_attachments_storage_limit = 0
    members_group.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert response.status_code == 200


@override_dynamic_settings(unused_attachments_storage_limit=0)
def test_account_attachments_shows_storage_for_user_with_used_and_unused_attachments_and_no_unused_limits(
    user, members_group, user_client, attachment, user_attachment, post
):
    attachment.uploader = user
    attachment.category = post.category
    attachment.thread = post.thread
    attachment.post = post
    attachment.save()

    members_group.unused_attachments_storage_limit = 0
    members_group.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert response.status_code == 200


def test_account_attachments_shows_storage_for_user_without_attachments_and_no_storage_limit(
    members_group, user_client
):
    members_group.attachment_storage_limit = 0
    members_group.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert response.status_code == 200


def test_account_attachments_shows_storage_for_user_with_used_attachment_and_no_storage_limit(
    user, members_group, user_client, attachment, post
):
    attachment.uploader = user
    attachment.category = post.category
    attachment.thread = post.thread
    attachment.post = post
    attachment.save()

    members_group.attachment_storage_limit = 0
    members_group.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert response.status_code == 200


def test_account_attachments_shows_storage_for_user_with_unused_attachment_and_no_storage_limit(
    user, members_group, user_client, attachment
):
    attachment.uploader = user
    attachment.save()

    members_group.attachment_storage_limit = 0
    members_group.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert response.status_code == 200


def test_account_attachments_shows_storage_for_user_with_used_and_unused_attachments_and_no_storage_limit(
    user, members_group, user_client, attachment, user_attachment, post
):
    attachment.uploader = user
    attachment.category = post.category
    attachment.thread = post.thread
    attachment.post = post
    attachment.save()

    members_group.attachment_storage_limit = 0
    members_group.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert response.status_code == 200


@override_dynamic_settings(unused_attachments_lifetime=12)
def test_account_attachments_shows_unused_attachments_expire_in_12_hours(
    user, user_client, attachment
):
    attachment.uploader = user
    attachment.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert_contains(response, "12 hours")


@override_dynamic_settings(unused_attachments_lifetime=48)
def test_account_attachments_shows_unused_attachments_expire_in_two_days(
    user, user_client, attachment
):
    attachment.uploader = user
    attachment.save()

    response = user_client.get(reverse("misago:account-attachments"))
    print(response.content.decode())
    assert_contains(response, "2 days")


def test_account_attachments_list_shows_blankslate_for_user_without_attachments(
    user_client,
):
    response = user_client.get(reverse("misago:account-attachments"))
    assert_contains(
        response, "You haven’t uploaded any attachments, or they have been deleted."
    )


def test_account_attachments_list_shows_broken_attachment(
    user, attachment, user_client
):
    attachment.uploader = user
    attachment.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert_contains(response, attachment.name)
    assert_contains(response, attachment.get_absolute_url())


def test_account_attachments_list_shows_image_attachment(user, attachment, user_client):
    attachment.uploader = user
    attachment.upload = "test.png"
    attachment.filetype_id = "png"
    attachment.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert_contains(response, attachment.name)
    assert_contains(response, attachment.get_absolute_url())


def test_account_attachments_list_shows_image_attachment_with_thumbnail(
    user, attachment, user_client
):
    attachment.uploader = user
    attachment.upload = "test.png"
    attachment.thumbnail = "thumbnail.png"
    attachment.filetype_id = "png"
    attachment.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert_contains(response, attachment.name)
    assert_contains(response, attachment.get_thumbnail_url())
    assert_contains(response, attachment.get_absolute_url())


def test_account_attachments_list_shows_video_attachment(user, attachment, user_client):
    attachment.uploader = user
    attachment.upload = "video.mp4"
    attachment.filetype_id = "mp4"
    attachment.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert_contains(response, attachment.name)
    assert_contains(response, attachment.get_absolute_url())


def test_account_attachments_list_shows_file_attachment(user, attachment, user_client):
    attachment.uploader = user
    attachment.upload = "document.pdf"
    attachment.filetype_id = "pdf"
    attachment.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert_contains(response, attachment.name)
    assert_contains(response, attachment.get_absolute_url())


def test_account_attachments_list_shows_attachment_delete_option_if_user_has_permission(
    user, attachment, user_client
):
    attachment.uploader = user
    attachment.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert_contains(response, attachment.name)
    assert_contains(response, attachment.get_delete_url())


def test_account_attachments_list_hides_attachment_delete_option_if_user_has_no_permission(
    user, members_group, attachment, user_client, post
):
    members_group.can_always_delete_own_attachments = False
    members_group.save()

    attachment.uploader = user
    attachment.category = post.category
    attachment.thread = post.thread
    attachment.post = post
    attachment.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert_contains(response, attachment.name)
    assert_not_contains(response, attachment.get_delete_url())


def test_account_attachments_list_excludes_anonymous_attachments(
    attachment, user_client
):
    attachment.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert_not_contains(response, attachment.name)


def test_account_attachments_list_excludes_other_users_attachments(
    other_user, attachment, user_client
):
    attachment.uploader = other_user
    attachment.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert_not_contains(response, attachment.name)


def test_account_attachments_list_excludes_user_deleted_attachments(
    user, attachment, user_client
):
    attachment.uploader = user
    attachment.is_deleted = True
    attachment.save()

    response = user_client.get(reverse("misago:account-attachments"))
    assert_not_contains(response, attachment.name)


@patch(
    "misago.account.views.settings.paginate_queryset", side_effect=EmptyPageError(10)
)
def test_account_attachments_list_redirects_to_last_page_for_invalid_cursor(
    mock_pagination, user_client
):
    response = user_client.get(reverse("misago:account-attachments"))

    assert response.status_code == 302
    assert response["location"] == reverse("misago:account-attachments") + "?cursor=10"

    mock_pagination.assert_called_once()
