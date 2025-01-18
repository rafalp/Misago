from django.urls import reverse

from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains


def test_attachment_details_view_renders_page_for_text_attachment(
    user, user_client, text_file, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user)
    response = user_client.get(attachment.get_details_url())

    assert_contains(response, attachment.name)


def test_attachment_details_view_renders_page_for_image_attachment(
    user, user_client, image_small, attachment_factory
):
    attachment = attachment_factory(image_small, uploader=user)
    response = user_client.get(attachment.get_details_url())

    assert_contains(response, attachment.name)


def test_attachment_details_view_returns_404_response_if_upload_is_missing(
    user_client, user_attachment
):
    response = user_client.get(user_attachment.get_details_url())
    assert response.status_code == 404


def test_attachment_details_view_returns_404_response_if_attachment_with_id_doesnt_exist(
    user_client,
):
    response = user_client.get(
        reverse(
            "misago:attachment-details",
            kwargs={"id": 1, "slug": "invalid"},
        )
    )
    assert response.status_code == 404


def test_attachment_details_view_returns_404_response_if_attachment_slug_is_invalid(
    user, user_client, text_file, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user)

    response = user_client.get(
        reverse(
            "misago:attachment-details",
            kwargs={"id": attachment.id, "slug": "invalid"},
        )
    )
    assert response.status_code == 404


def test_attachment_details_view_returns_404_response_for_user_if_attachment_is_deleted(
    user, user_client, text_file, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user, is_deleted=True)

    response = user_client.get(attachment.get_details_url())
    assert response.status_code == 404


def test_attachment_details_view_returns_404_response_for_anonymous_user_if_attachment_is_deleted(
    user, client, text_file, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user, is_deleted=True)

    response = client.get(attachment.get_details_url())
    assert response.status_code == 404


def test_attachment_details_view_renders_page_for_admin_if_attachment_is_deleted(
    user, admin_client, text_file, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user, is_deleted=True)

    response = admin_client.get(attachment.get_details_url())
    assert_contains(response, attachment.name)


def test_attachment_details_view_checks_user_permissions(
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

    response = user_client.get(attachment.get_details_url())
    assert_contains(
        response,
        "You can&#x27;t download attachments in this category.",
        status_code=403,
    )
