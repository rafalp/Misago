from django.urls import reverse

from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains, assert_not_contains


def test_attachment_details_view_renders_page_for_text_attachment(
    user_client, user_text_attachment
):
    response = user_client.get(user_text_attachment.get_details_url())
    assert_contains(response, user_text_attachment.name)


def test_attachment_details_view_renders_page_for_image_attachment(
    user_client, user_image_attachment
):
    response = user_client.get(user_image_attachment.get_details_url())
    assert_contains(response, user_image_attachment.name)


def test_attachment_details_view_renders_page_for_video_attachment(
    user_client, user_video_attachment
):
    response = user_client.get(user_video_attachment.get_details_url())
    assert_contains(response, user_video_attachment.name)


def test_attachment_details_view_renders_page_with_delete_option(
    user_client, user_text_attachment
):
    response = user_client.get(user_text_attachment.get_details_url())
    assert_contains(response, user_text_attachment.name)
    assert_contains(response, user_text_attachment.get_delete_url())


def test_attachment_details_view_renders_page_without_delete_option(
    user_client, text_attachment, post
):
    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = user_client.get(text_attachment.get_details_url())
    assert_contains(response, text_attachment.name)
    assert_not_contains(response, text_attachment.get_delete_url())


def test_attachment_details_view_renders_page_without_post_link_for_unused_attachment(
    user_client, user_text_attachment
):
    response = user_client.get(user_text_attachment.get_details_url())
    assert_contains(response, user_text_attachment.name)
    assert_not_contains(response, "/post/")


def test_attachment_details_view_renders_page_with_post_link_for_user_attachment(
    user_client, text_attachment, post
):
    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = user_client.get(text_attachment.get_details_url())
    assert_contains(response, text_attachment.name)
    assert_contains(response, "/post/")
    assert_contains(response, post.get_absolute_url())


def test_attachment_details_view_renders_page_without_post_link_if_user_has_no_post_permission(
    user_client, user_text_attachment, post
):
    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    post.is_hidden = True
    post.save()

    response = user_client.get(user_text_attachment.get_details_url())
    assert_contains(response, user_text_attachment.name)
    assert_not_contains(response, "/post/")
    assert_not_contains(response, post.get_absolute_url())


def test_attachment_details_view_returns_404_response_if_upload_is_missing(
    user_client, user_broken_text_attachment
):
    response = user_client.get(user_broken_text_attachment.get_details_url())
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


def test_attachment_details_view_returns_301_response_if_attachment_slug_is_invalid(
    user_client, user_text_attachment
):
    response = user_client.get(
        reverse(
            "misago:attachment-details",
            kwargs={"id": user_text_attachment.id, "slug": "invalid"},
        )
    )
    assert response.status_code == 301
    assert response["location"] == user_text_attachment.get_details_url()


def test_attachment_details_view_returns_404_response_for_user_if_attachment_is_deleted(
    user_client, user_text_attachment
):
    user_text_attachment.is_deleted = True
    user_text_attachment.save()

    response = user_client.get(user_text_attachment.get_details_url())
    assert response.status_code == 404


def test_attachment_details_view_returns_404_response_for_anonymous_user_if_attachment_is_deleted(
    client, user_text_attachment
):
    user_text_attachment.is_deleted = True
    user_text_attachment.save()

    response = client.get(user_text_attachment.get_details_url())
    assert response.status_code == 404


def test_attachment_details_view_renders_page_for_admin_if_attachment_is_deleted(
    admin_client, text_attachment
):
    text_attachment.is_deleted = True
    text_attachment.save()

    response = admin_client.get(text_attachment.get_details_url())
    assert_contains(response, text_attachment.name)


def test_attachment_details_view_checks_user_permissions(
    other_user_text_attachment, members_group, user_client, post
):
    CategoryGroupPermission.objects.filter(
        group=members_group,
        permission=CategoryPermission.ATTACHMENTS,
    ).delete()

    other_user_text_attachment.associate_with_post(post)
    other_user_text_attachment.save()

    response = user_client.get(other_user_text_attachment.get_details_url())
    assert_contains(
        response,
        "You can&#x27;t download attachments in this category.",
        status_code=403,
    )
