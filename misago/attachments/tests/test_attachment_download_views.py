from django.urls import reverse

from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains


def test_attachment_download_view_returns_server_response(
    user, user_client, text_file, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user)
    response = user_client.get(attachment.get_absolute_url())

    assert response.status_code == 301
    assert response["location"] == attachment.upload.url


def test_attachment_download_view_returns_404_response_if_upload_is_missing(
    user_client, user_broken_text_attachment
):
    response = user_client.get(user_broken_text_attachment.get_absolute_url())
    assert response.status_code == 404


def test_attachment_thumbnail_view_returns_server_response(
    user, user_client, image_small, attachment_factory
):
    attachment = attachment_factory(
        image_small, uploader=user, thumbnail_path=image_small
    )
    response = user_client.get(attachment.get_thumbnail_url())

    assert response.status_code == 301
    assert response["location"] == attachment.thumbnail.url


def test_attachment_thumbnail_view_returns_404_response_if_thumbnail_is_missing(
    user, user_client, image_small, attachment_factory
):
    attachment = attachment_factory(image_small, uploader=user)
    response = user_client.get(attachment.get_thumbnail_url())

    assert response.status_code == 404


def test_attachment_download_view_returns_404_response_if_attachment_with_id_doesnt_exist(
    user_client,
):
    response = user_client.get(
        reverse(
            "misago:attachment-download",
            kwargs={"id": 1, "slug": "invalid"},
        )
    )
    assert response.status_code == 404


def test_attachment_thumbnail_view_returns_404_response_if_attachment_with_id_doesnt_exist(
    user_client,
):
    response = user_client.get(
        reverse(
            "misago:attachment-thumbnail",
            kwargs={"id": 1, "slug": "invalid"},
        )
    )
    assert response.status_code == 404


def test_attachment_download_view_returns_301_response_if_attachment_slug_is_invalid(
    user, user_client, text_file, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user)

    response = user_client.get(
        reverse(
            "misago:attachment-download",
            kwargs={"id": attachment.id, "slug": "invalid"},
        )
    )
    assert response.status_code == 301
    assert response["location"] == attachment.get_absolute_url()


def test_attachment_thumbnail_view_returns_301_response_if_attachment_slug_is_invalid(
    user, user_client, image_small, attachment_factory
):
    attachment = attachment_factory(
        image_small, uploader=user, thumbnail_path=image_small
    )
    response = user_client.get(
        reverse(
            "misago:attachment-thumbnail",
            kwargs={"id": attachment.id, "slug": "invalid"},
        )
    )
    assert response.status_code == 301
    assert response["location"] == attachment.get_thumbnail_url()


def test_attachment_download_view_returns_404_response_for_user_if_attachment_is_deleted(
    user, user_client, text_file, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user, is_deleted=True)

    response = user_client.get(attachment.get_absolute_url())
    assert response.status_code == 404


def test_attachment_thumbnail_view_returns_404_response_for_user_if_attachment_is_deleted(
    user, user_client, image_small, attachment_factory
):
    attachment = attachment_factory(
        image_small, uploader=user, thumbnail_path=image_small, is_deleted=True
    )
    response = user_client.get(attachment.get_thumbnail_url())
    assert response.status_code == 404


def test_attachment_download_view_returns_404_response_for_anonymous_user_if_attachment_is_deleted(
    user, client, text_file, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user, is_deleted=True)

    response = client.get(attachment.get_absolute_url())
    assert response.status_code == 404


def test_attachment_thumbnail_view_returns_404_response_for_anonymous_user_if_attachment_is_deleted(
    user, client, image_small, attachment_factory
):
    attachment = attachment_factory(
        image_small, uploader=user, thumbnail_path=image_small, is_deleted=True
    )
    response = client.get(attachment.get_thumbnail_url())
    assert response.status_code == 404


def test_attachment_download_view_returns_server_response_for_admin_if_attachment_is_deleted(
    user, admin_client, text_file, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user, is_deleted=True)

    response = admin_client.get(attachment.get_absolute_url())
    assert response.status_code == 301
    assert response["location"] == attachment.upload.url


def test_attachment_thumbnail_view_returns_server_response_for_admin_if_attachment_is_deleted(
    user, admin_client, image_small, attachment_factory
):
    attachment = attachment_factory(
        image_small, uploader=user, thumbnail_path=image_small, is_deleted=True
    )
    response = admin_client.get(attachment.get_thumbnail_url())
    assert response.status_code == 301
    assert response["location"] == attachment.thumbnail.url


def test_attachment_download_view_checks_user_permissions(
    other_user,
    members_group,
    user_client,
    text_file,
    attachment_factory,
    post,
):
    CategoryGroupPermission.objects.filter(
        group=members_group,
        permission=CategoryPermission.ATTACHMENTS,
    ).delete()

    attachment = attachment_factory(
        text_file,
        uploader=other_user,
        post=post,
    )

    response = user_client.get(attachment.get_absolute_url())
    assert_contains(
        response,
        "You can&#x27;t download attachments in this category.",
        status_code=403,
    )


def test_attachment_thumbnail_view_checks_user_permissions(
    other_user,
    members_group,
    user_client,
    image_small,
    attachment_factory,
    post,
):
    CategoryGroupPermission.objects.filter(
        group=members_group,
        permission=CategoryPermission.ATTACHMENTS,
    ).delete()

    attachment = attachment_factory(
        image_small,
        uploader=other_user,
        thumbnail_path=image_small,
        post=post,
    )
    response = user_client.get(attachment.get_thumbnail_url())
    assert_contains(
        response,
        "You can&#x27;t download attachments in this category.",
        status_code=403,
    )
