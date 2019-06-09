from io import BytesIO

import pytest
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from ... import settings
from ...models import Setting

admin_link = reverse("misago:admin:settings:users:index")


def create_image(width, height):
    image = Image.new("RGBA", (width, height))
    stream = BytesIO()
    image.save(stream, "PNG")
    stream.seek(0)
    return SimpleUploadedFile("image.png", stream.read(), "image/jpeg")


def submit_image(admin_client, image=""):
    data = {
        "account_activation": "user",
        "username_length_min": 10,
        "username_length_max": 10,
        "anonymous_username": "Deleted",
        "avatar_upload_limit": 2000,
        "default_avatar": "gravatar",
        "default_gravatar_fallback": "dynamic",
        "signature_length_max": 100,
        "blank_avatar": image,
        "subscribe_start": "no",
        "subscribe_reply": "no",
        "users_per_page": 12,
        "users_per_page_orphans": 4,
        "top_posters_ranking_length": 10,
        "top_posters_ranking_size": 10,
        "allow_data_downloads": "no",
        "data_downloads_expiration": 48,
        "allow_delete_own_account": "no",
        "new_inactive_accounts_delete": 0,
        "ip_storage_time": 0,
    }

    return admin_client.post(admin_link, data)


@pytest.fixture
def setting(db):
    return Setting.objects.get(setting="blank_avatar")


@pytest.fixture
def setting_with_value(admin_client, setting):
    min_size = max(settings.MISAGO_AVATARS_SIZES)
    image_file = create_image(min_size, min_size)
    submit_image(admin_client, image_file)

    setting.refresh_from_db()
    return setting


def test_uploaded_image_is_rejected_if_its_not_square(admin_client, setting):
    image_file = create_image(100, 200)
    submit_image(admin_client, image_file)

    setting.refresh_from_db()
    assert not setting.value


def test_uploaded_image_is_rejected_if_its_smaller_than_max_avatar_size(
    admin_client, setting
):
    min_size = max(settings.MISAGO_AVATARS_SIZES)
    image_file = create_image(min_size - 1, min_size - 1)
    submit_image(admin_client, image_file)

    setting.refresh_from_db()
    assert not setting.value


def test_valid_blank_avatar_can_be_uploaded(admin_client, setting):
    min_size = max(settings.MISAGO_AVATARS_SIZES)
    image_file = create_image(min_size, min_size)
    submit_image(admin_client, image_file)

    setting.refresh_from_db()
    assert setting.value


def test_submitting_form_without_new_image_doesnt_unset_existing_image(
    admin_client, setting_with_value
):
    submit_image(admin_client)
    setting_with_value.refresh_from_db()
    assert setting_with_value.value
