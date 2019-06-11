import os

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from ...models import Icon


@pytest.fixture
def favicon(db, image_alt):
    return Icon.objects.create(
        type=Icon.TYPE_FAVICON,
        image=SimpleUploadedFile("favicon.png", image_alt, "image/png"),
    )


@pytest.fixture
def favicon_32(db, image_alt):
    return Icon.objects.create(
        type=Icon.TYPE_FAVICON_32,
        image=SimpleUploadedFile("favicon-32.png", image_alt, "image/png"),
    )


@pytest.fixture
def favicon_16(db, image_alt):
    return Icon.objects.create(
        type=Icon.TYPE_FAVICON_16,
        image=SimpleUploadedFile("favicon-16.png", image_alt, "image/png"),
    )


def test_uploading_favicon_sets_favicon_images(admin_client, admin_link, image):
    admin_client.post(
        admin_link, {"favicon": SimpleUploadedFile("image.png", image, "image/png")}
    )
    Icon.objects.get(type=Icon.TYPE_FAVICON)
    Icon.objects.get(type=Icon.TYPE_FAVICON_32)
    Icon.objects.get(type=Icon.TYPE_FAVICON_16)


def test_uploading_favicon_removes_existing_favicon_images(
    admin_client, admin_link, image, favicon, favicon_32, favicon_16
):
    admin_client.post(
        admin_link, {"favicon": SimpleUploadedFile("image.png", image, "image/png")}
    )

    with pytest.raises(Icon.DoesNotExist):
        favicon.refresh_from_db()

    with pytest.raises(Icon.DoesNotExist):
        favicon_32.refresh_from_db()

    with pytest.raises(Icon.DoesNotExist):
        favicon_16.refresh_from_db()


def test_uploading_new_favicon_removes_old_one_image_file(
    admin_client, admin_link, image, favicon, favicon_32, favicon_16
):
    admin_client.post(
        admin_link, {"favicon": SimpleUploadedFile("image.png", image, "image/png")}
    )

    assert not os.path.exists(favicon.image.path)
    assert not os.path.exists(favicon_32.image.path)
    assert not os.path.exists(favicon_16.image.path)


def test_submitting_form_without_new_icon_does_not_delete_old_favicon_images(
    admin_client, admin_link, favicon, favicon_32, favicon_16
):
    admin_client.post(admin_link, {})
    favicon.refresh_from_db()
    favicon_32.refresh_from_db()
    favicon_16.refresh_from_db()


def test_favicon_can_be_deleted_without_setting_new_one(
    admin_client, admin_link, favicon, favicon_32, favicon_16
):
    admin_client.post(admin_link, {"favicon_delete": "1"})

    with pytest.raises(Icon.DoesNotExist):
        favicon.refresh_from_db()

    with pytest.raises(Icon.DoesNotExist):
        favicon_32.refresh_from_db()

    with pytest.raises(Icon.DoesNotExist):
        favicon_16.refresh_from_db()


def test_deleting_icon_also_deletes_its_image_files(
    admin_client, admin_link, favicon, favicon_32, favicon_16
):
    admin_client.post(admin_link, {"favicon_delete": "1"})
    assert not os.path.exists(favicon.image.path)
    assert not os.path.exists(favicon_32.image.path)
    assert not os.path.exists(favicon_16.image.path)


def test_uploading_invalid_icon_does_not_remove_current_icon(
    admin_client, admin_link, favicon, favicon_32, favicon_16, image_small
):
    admin_client.post(
        admin_link,
        {"favicon": SimpleUploadedFile("image.png", image_small, "image/png")},
    )

    favicon.refresh_from_db()
    favicon_32.refresh_from_db()
    favicon_16.refresh_from_db()


def test_icon_is_not_set_because_it_was_not_square(
    admin_client, admin_link, image_non_square
):
    admin_client.post(
        admin_link,
        {"favicon": SimpleUploadedFile("image.png", image_non_square, "image/png")},
    )

    assert not Icon.objects.exists()


def test_icon_is_not_set_because_it_was_too_small(
    admin_client, admin_link, image_small
):
    admin_client.post(
        admin_link,
        {"favicon": SimpleUploadedFile("image.png", image_small, "image/png")},
    )

    assert not Icon.objects.exists()
