import pytest
from django.urls import reverse

from ...acl.models import Role
from ...acl.test import patch_user_acl
from ...conf import settings
from ...conf.test import override_dynamic_settings
from ..models import Attachment, AttachmentType
from ..test import post_thread


@pytest.fixture
def attachment_type(db):
    return AttachmentType.objects.order_by("id").first()


@pytest.fixture
def attachment(attachment_type, post, user):
    return Attachment.objects.create(
        secret="secret",
        filetype=attachment_type,
        post=post,
        uploader=user,
        uploader_name=user.username,
        uploader_slug=user.slug,
        filename="test.txt",
        file="test.txt",
        size=1000,
    )


@pytest.fixture
def image(post, user):
    return Attachment.objects.create(
        secret="secret",
        filetype=AttachmentType.objects.get(mimetypes="image/png"),
        post=post,
        uploader=user,
        uploader_name=user.username,
        uploader_slug=user.slug,
        filename="test.png",
        image="test.png",
        size=1000,
    )


@pytest.fixture
def image_with_thumbnail(post, user):
    return Attachment.objects.create(
        secret="secret",
        filetype=AttachmentType.objects.get(mimetypes="image/png"),
        post=post,
        uploader=user,
        uploader_name=user.username,
        uploader_slug=user.slug,
        filename="test.png",
        image="test.png",
        thumbnail="test-thumbnail.png",
        size=1000,
    )


@pytest.fixture
def other_users_attachment(attachment, other_user):
    attachment.uploader = other_user
    attachment.save()
    return attachment


@pytest.fixture
def orphaned_attachment(attachment):
    attachment.post = None
    attachment.save()
    return attachment


@pytest.fixture
def other_users_orphaned_attachment(other_users_attachment):
    other_users_attachment.post = None
    other_users_attachment.save()
    return other_users_attachment


def assert_403(response):
    assert response.status_code == 302
    assert response["location"].endswith(settings.MISAGO_ATTACHMENT_403_IMAGE)


def assert_404(response):
    assert response.status_code == 302
    assert response["location"].endswith(settings.MISAGO_ATTACHMENT_404_IMAGE)


def test_proxy_redirects_client_to_attachment_file(client, attachment):
    response = client.get(attachment.get_absolute_url())
    assert response.status_code == 302
    assert response["location"].endswith("test.txt")


def test_proxy_redirects_client_to_attachment_image(client, image):
    response = client.get(image.get_absolute_url())
    assert response.status_code == 302
    assert response["location"].endswith("test.png")


def test_proxy_redirects_client_to_attachment_thumbnail(client, image_with_thumbnail):
    response = client.get(image_with_thumbnail.get_thumbnail_url())
    assert response.status_code == 302
    assert response["location"].endswith("test-thumbnail.png")


def test_proxy_redirects_to_404_image_for_nonexistant_attachment(db, client):
    response = client.get(
        reverse("misago:attachment", kwargs={"pk": 1, "secret": "secret"})
    )
    assert_404(response)


def test_proxy_redirects_to_404_image_for_url_with_invalid_attachment_secret(
    client, attachment
):
    response = client.get(
        reverse("misago:attachment", kwargs={"pk": attachment.id, "secret": "invalid"})
    )
    assert_404(response)


@patch_user_acl({"can_download_other_users_attachments": False})
def test_proxy_redirects_to_403_image_for_user_without_permission_to_see_attachment(
    user_client, other_users_attachment
):
    response = user_client.get(other_users_attachment.get_absolute_url())
    assert_403(response)


def test_thumbnail_proxy_redirects_to_404_for_non_image_attachment(client, attachment):
    response = client.get(
        reverse(
            "misago:attachment-thumbnail",
            kwargs={"pk": attachment.pk, "secret": attachment.secret},
        )
    )
    assert_404(response)


def test_thumbnail_proxy_redirects_to_regular_image_for_image_without_thumbnail(
    client, image
):
    response = client.get(
        reverse(
            "misago:attachment-thumbnail",
            kwargs={"pk": image.pk, "secret": image.secret},
        )
    )
    assert response.status_code == 302
    assert response["location"].endswith("test.png")


def test_thumbnail_proxy_redirects_to_thumbnail_image(client, image_with_thumbnail):
    response = client.get(
        reverse(
            "misago:attachment-thumbnail",
            kwargs={
                "pk": image_with_thumbnail.pk,
                "secret": image_with_thumbnail.secret,
            },
        )
    )
    assert response.status_code == 302
    assert response["location"].endswith("test-thumbnail.png")


def test_proxy_blocks_user_from_their_orphaned_attachment(
    user_client, orphaned_attachment
):
    response = user_client.get(orphaned_attachment.get_absolute_url())
    assert_404(response)


def test_proxy_redirects_user_to_their_orphaned_attachment_if_link_has_shva_key(
    user_client, orphaned_attachment
):
    response = user_client.get("%s?shva=1" % orphaned_attachment.get_absolute_url())
    assert response.status_code == 302
    assert response["location"].endswith("test.txt")


def test_proxy_blocks_user_from_other_users_orphaned_attachment(
    user_client, other_users_orphaned_attachment
):
    response = user_client.get(other_users_orphaned_attachment.get_absolute_url())
    assert_404(response)


def test_proxy_blocks_user_from_other_users_orphaned_attachment_if_link_has_shva_key(
    user_client, other_users_orphaned_attachment
):
    response = user_client.get(
        "%s?shva=1" % other_users_orphaned_attachment.get_absolute_url()
    )
    assert_404(response)


def test_proxy_redirects_staff_to_other_users_orphaned_attachment(
    staff_client, orphaned_attachment
):
    response = staff_client.get("%s?shva=1" % orphaned_attachment.get_absolute_url())
    assert response.status_code == 302
    assert response["location"].endswith("test.txt")


def test_proxy_blocks_user_from_attachment_with_disabled_type(
    user_client, attachment, attachment_type
):
    attachment_type.status = AttachmentType.DISABLED
    attachment_type.save()

    response = user_client.get(attachment.get_absolute_url())
    assert_403(response)


@pytest.fixture
def role(db):
    return Role.objects.create(name="Test")


@pytest.fixture
def limited_attachment_type(attachment_type, role):
    attachment_type.limit_downloads_to.add(role)
    return attachment_type


def test_proxy_blocks_user_without_role_from_attachment_with_limited_type(
    user_client, attachment, limited_attachment_type
):
    response = user_client.get(attachment.get_absolute_url())
    assert_403(response)


def test_proxy_allows_user_with_role_to_download_attachment_with_limited_type(
    user, user_client, role, attachment, limited_attachment_type
):
    user.roles.add(role)
    response = user_client.get(attachment.get_absolute_url())
    assert response.status_code == 302
    assert response["location"].endswith("test.txt")


def test_proxy_allows_staff_user_without_role_to_download_attachment_with_limited_type(
    staff_client, role, attachment, limited_attachment_type
):
    response = staff_client.get(attachment.get_absolute_url())
    assert response.status_code == 302
    assert response["location"].endswith("test.txt")


@override_dynamic_settings(attachment_403_image="custom-403-image.png")
@patch_user_acl({"can_download_other_users_attachments": False})
def test_proxy_uses_custom_permission_denied_image_if_one_is_set(
    user_client, other_users_attachment
):
    response = user_client.get(other_users_attachment.get_absolute_url())
    assert response.status_code == 302
    assert response["location"].endswith("custom-403-image.png")


@override_dynamic_settings(attachment_404_image="custom-404-image.png")
def test_proxy_uses_custom_not_found_image_if_one_is_set(db, client):
    response = client.get(
        reverse("misago:attachment", kwargs={"pk": 1, "secret": "secret"})
    )
    assert response.status_code == 302
    assert response["location"].endswith("custom-404-image.png")
