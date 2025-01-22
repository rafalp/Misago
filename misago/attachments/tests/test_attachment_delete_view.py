import pytest
from django.urls import reverse

from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains
from ..models import Attachment


def test_attachment_delete_view_renders_confirmation_for_attachment_on_get(
    user, user_client, attachment
):
    attachment.uploader = user
    attachment.save()

    response = user_client.get(attachment.get_delete_url())

    assert_contains(response, attachment.name)


def test_attachment_delete_view_deletes_attachment_on_post(
    user, user_client, attachment
):
    attachment.uploader = user
    attachment.save()

    response = user_client.post(attachment.get_delete_url())
    assert response.status_code == 302
    assert response["location"] == reverse("misago:index")

    with pytest.raises(Attachment.DoesNotExist):
        attachment.refresh_from_db()


def test_attachment_delete_view_redirects_to_attachment_post_if_post_referer_is_set(
    user, user_client, attachment, post
):
    attachment.category = post.category
    attachment.thread = post.thread
    attachment.post = post
    attachment.uploader = user
    attachment.save()

    response = user_client.post(attachment.get_delete_url() + "?referer=post")
    assert response.status_code == 302
    assert response["location"] == post.get_absolute_url()

    with pytest.raises(Attachment.DoesNotExist):
        attachment.refresh_from_db()


def test_attachment_delete_view_redirects_to_index_if_post_referer_is_set_but_post_is_unused(
    user, user_client, attachment, post
):
    attachment.uploader = user
    attachment.save()

    response = user_client.post(attachment.get_delete_url() + "?referer=post")
    assert response.status_code == 302
    assert response["location"] == reverse("misago:index")

    with pytest.raises(Attachment.DoesNotExist):
        attachment.refresh_from_db()


def test_attachment_delete_view_redirects_to_account_settings_if_settings_referer_is_set(
    user, user_client, attachment, post
):
    attachment.category = post.category
    attachment.thread = post.thread
    attachment.post = post
    attachment.uploader = user
    attachment.save()

    response = user_client.post(attachment.get_delete_url() + "?referer=settings")
    assert response.status_code == 302
    assert response["location"] == reverse("misago:account-attachments")

    with pytest.raises(Attachment.DoesNotExist):
        attachment.refresh_from_db()


def test_attachment_delete_view_redirects_to_account_settings_after_page_if_settings_referer_is_set(
    user, user_client, attachment, post
):
    attachment.category = post.category
    attachment.thread = post.thread
    attachment.post = post
    attachment.uploader = user
    attachment.save()

    response = user_client.post(
        attachment.get_delete_url() + "?referer=settings&after=123"
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:account-attachments") + "?after=123"

    with pytest.raises(Attachment.DoesNotExist):
        attachment.refresh_from_db()


def test_attachment_delete_view_redirects_to_account_settings_before_page_if_settings_referer_is_set(
    user, user_client, attachment, post
):
    attachment.category = post.category
    attachment.thread = post.thread
    attachment.post = post
    attachment.uploader = user
    attachment.save()

    response = user_client.post(
        attachment.get_delete_url() + "?referer=settings&before=123"
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:account-attachments") + "?before=123"

    with pytest.raises(Attachment.DoesNotExist):
        attachment.refresh_from_db()


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


def test_attachment_delete_view_returns_404_response_if_attachment_slug_is_invalid(
    user, user_client, attachment
):
    attachment.uploader = user
    attachment.save()

    response = user_client.get(
        reverse(
            "misago:attachment-delete",
            kwargs={"id": attachment.id, "slug": "invalid"},
        )
    )
    assert response.status_code == 404


def test_attachment_delete_view_checks_delete_attachment_permissions(
    other_user,
    user_client,
    attachment,
    post,
):
    attachment.category = post.category
    attachment.thread = post.thread
    attachment.post = post
    attachment.uploader = other_user
    attachment.save()

    response = user_client.get(attachment.get_delete_url())

    assert_contains(
        response,
        "You can&#x27;t delete other users attachments.",
        status_code=403,
    )
