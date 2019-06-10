import os

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from ...models import Icon


@pytest.fixture
def apple_touch_icon(db, image):
    return Icon.objects.create(
        type=Icon.TYPE_APPLE_TOUCH_ICON,
        image=SimpleUploadedFile("image.png", image, "image/png"),
    )


def test_new_touch_icon_can_be_set(admin_client, admin_link, image):
    admin_client.post(
        admin_link,
        {"apple_touch_icon": SimpleUploadedFile("image.png", image, "image/png")},
    )
    Icon.objects.get(type=Icon.TYPE_APPLE_TOUCH_ICON)


def test_setting_new_touch_icon_removes_old_one(
    admin_client, admin_link, image, apple_touch_icon
):
    admin_client.post(
        admin_link,
        {"apple_touch_icon": SimpleUploadedFile("image.png", image, "image/png")},
    )

    with pytest.raises(Icon.DoesNotExist):
        apple_touch_icon.refresh_from_db()


def test_setting_new_touch_icon_removes_old_one_image_file(
    admin_client, admin_link, image, apple_touch_icon
):
    admin_client.post(
        admin_link,
        {"apple_touch_icon": SimpleUploadedFile("image.png", image, "image/png")},
    )

    assert not os.path.exists(apple_touch_icon.image.path)


def test_submitting_form_without_new_icon_does_not_delete_old_one(
    admin_client, admin_link, apple_touch_icon
):
    admin_client.post(admin_link, {})
    apple_touch_icon.refresh_from_db()


def test_icon_can_be_deleted_without_setting_new_one(
    admin_client, admin_link, apple_touch_icon
):
    admin_client.post(admin_link, {"apple_touch_icon_delete": "1"})

    with pytest.raises(Icon.DoesNotExist):
        apple_touch_icon.refresh_from_db()


def test_deleting_icon_also_deletes_its_image_file(
    admin_client, admin_link, apple_touch_icon
):
    admin_client.post(admin_link, {"apple_touch_icon_delete": "1"})
    assert not os.path.exists(apple_touch_icon.image.path)


def test_uploading_invalid_icon_does_not_remove_current_icon(
    admin_client, admin_link, apple_touch_icon, image_small
):
    admin_client.post(
        admin_link,
        {"apple_touch_icon": SimpleUploadedFile("image.png", image_small, "image/png")},
    )

    apple_touch_icon.refresh_from_db()


def test_icon_is_not_set_because_it_was_not_square(
    admin_client, admin_link, image_non_square
):
    admin_client.post(
        admin_link,
        {
            "apple_touch_icon": SimpleUploadedFile(
                "image.png", image_non_square, "image/png"
            )
        },
    )

    assert not Icon.objects.exists()


def test_icon_is_not_set_because_it_was_too_small(
    admin_client, admin_link, image_small
):
    admin_client.post(
        admin_link,
        {"apple_touch_icon": SimpleUploadedFile("image.png", image_small, "image/png")},
    )

    assert not Icon.objects.exists()
