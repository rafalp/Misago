import pytest
from django.urls import reverse

from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains
from ..models import Attachment


def test_attachment_delete_view_renders_confirmation_for_attachment_on_get(
    user_client, user_text_attachment
):
    response = user_client.get(user_text_attachment.get_delete_url())
    assert_contains(response, user_text_attachment.name)


def test_attachment_delete_view_deletes_attachment_on_post(
    user_client, user_text_attachment
):
    response = user_client.post(user_text_attachment.get_delete_url())
    assert response.status_code == 302
    assert response["location"] == reverse("misago:index")

    with pytest.raises(Attachment.DoesNotExist):
        user_text_attachment.refresh_from_db()


def test_attachment_delete_view_redirects_to_attachment_post_if_post_referrer_is_set(
    user_client, user_text_attachment, post
):
    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    response = user_client.post(
        user_text_attachment.get_delete_url() + "?referrer=post"
    )
    assert response.status_code == 302
    assert response["location"] == post.get_absolute_url()

    with pytest.raises(Attachment.DoesNotExist):
        user_text_attachment.refresh_from_db()


def test_attachment_delete_view_redirects_to_index_if_post_referrer_is_set_but_attachment_is_unused(
    user_client, user_text_attachment
):
    response = user_client.post(
        user_text_attachment.get_delete_url() + "?referrer=post"
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:index")

    with pytest.raises(Attachment.DoesNotExist):
        user_text_attachment.refresh_from_db()


def test_attachment_delete_view_redirects_to_account_settings_if_settings_referrer_is_set(
    user_client, user_text_attachment
):
    response = user_client.post(
        user_text_attachment.get_delete_url() + "?referrer=settings"
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:account-attachments")

    with pytest.raises(Attachment.DoesNotExist):
        user_text_attachment.refresh_from_db()


def test_attachment_delete_view_redirects_to_account_settings_page_if_settings_referrer_is_set(
    user_client, user_text_attachment
):
    response = user_client.post(
        user_text_attachment.get_delete_url() + "?referrer=settings&cursor=123"
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:account-attachments") + "?cursor=123"

    with pytest.raises(Attachment.DoesNotExist):
        user_text_attachment.refresh_from_db()


def test_attachment_delete_view_returns_404_response_if_attachment_is_already_deleted(
    user_client, user_text_attachment
):
    user_text_attachment.is_deleted = True
    user_text_attachment.save()

    response = user_client.get(user_text_attachment.get_delete_url())
    assert response.status_code == 404


def test_attachment_delete_view_returns_404_response_if_attachment_with_id_doesnt_exist(
    user_client,
):
    response = user_client.get(
        reverse(
            "misago:attachment-delete",
            kwargs={"id": 1, "slug": "invalid"},
        )
    )
    assert response.status_code == 404


def test_attachment_delete_view_returns_301_response_if_attachment_slug_is_invalid(
    user_client, user_text_attachment
):
    response = user_client.get(
        reverse(
            "misago:attachment-delete",
            kwargs={"id": user_text_attachment.id, "slug": "invalid"},
        )
        + "?referrer=settings"
    )
    assert response.status_code == 301
    assert (
        response["location"]
        == user_text_attachment.get_delete_url() + "?referrer=settings"
    )


def test_attachment_delete_view_checks_delete_attachment_permissions(
    user_client,
    other_user_text_attachment,
    post,
):
    other_user_text_attachment.associate_with_post(post)
    other_user_text_attachment.save()

    response = user_client.get(other_user_text_attachment.get_delete_url())

    assert_contains(
        response,
        "You can&#x27;t delete other users attachments.",
        status_code=403,
    )
