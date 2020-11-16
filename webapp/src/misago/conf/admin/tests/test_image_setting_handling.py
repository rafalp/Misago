import os

import pytest
from django.urls import reverse

from ....test import assert_contains
from ...models import Setting

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE = os.path.join(BASE_DIR, "testfiles", "image.png")
OTHER_IMAGE = os.path.join(BASE_DIR, "testfiles", "image-other.png")
OTHER_FILE = os.path.join(BASE_DIR, "testfiles", "other")


@pytest.fixture
def setting(db):
    obj = Setting.objects.get(setting="logo")
    yield obj
    obj.refresh_from_db()
    if obj.image:
        obj.image.delete(save=False)


def test_image_setting_can_be_set(admin_client, setting):
    with open(IMAGE, "rb") as image:
        admin_client.post(
            reverse("misago:admin:settings:general:index"),
            {"forum_name": "Misago", "forum_address": "http://test.com", "logo": image},
        )

    setting.refresh_from_db()
    assert setting.image


def test_setting_image_also_sets_its_dimensions(admin_client, setting):
    with open(IMAGE, "rb") as image:
        admin_client.post(
            reverse("misago:admin:settings:general:index"),
            {"forum_name": "Misago", "forum_address": "http://test.com", "logo": image},
        )

    setting.refresh_from_db()
    assert setting.image_width == 4
    assert setting.image_height == 2


def test_setting_image_filename_is_prefixed_with_setting_name(admin_client, setting):
    with open(IMAGE, "rb") as image:
        admin_client.post(
            reverse("misago:admin:settings:general:index"),
            {"forum_name": "Misago", "forum_address": "http://test.com", "logo": image},
        )

    setting.refresh_from_db()
    assert ("%s." % setting.setting) in str(setting.image.name)


def test_setting_image_filename_is_hashed(admin_client, setting):
    with open(IMAGE, "rb") as image:
        admin_client.post(
            reverse("misago:admin:settings:general:index"),
            {"forum_name": "Misago", "forum_address": "http://test.com", "logo": image},
        )

    setting.refresh_from_db()
    assert str(setting.image.name).endswith(".c68ed127.png")


def test_image_setting_rejects_non_image_file(admin_client, setting):
    with open(OTHER_FILE, "rb") as not_image:
        admin_client.post(
            reverse("misago:admin:settings:general:index"),
            {
                "forum_name": "Misago",
                "forum_address": "http://test.com",
                "logo": not_image,
            },
        )

    setting.refresh_from_db()
    assert not setting.image


@pytest.fixture
def setting_with_value(admin_client, setting):
    with open(IMAGE, "rb") as not_image:
        admin_client.post(
            reverse("misago:admin:settings:general:index"),
            {
                "forum_name": "Misago",
                "forum_address": "http://test.com",
                "logo": not_image,
            },
        )

    setting.refresh_from_db()
    return setting


def test_image_setting_value_is_rendered_in_form(admin_client, setting_with_value):
    response = admin_client.get(reverse("misago:admin:settings:general:index"))
    assert_contains(response, setting_with_value.image.url)


def test_invalid_file_is_not_set_as_value(admin_client, setting):
    with open(OTHER_FILE, "rb") as not_image:
        admin_client.post(
            reverse("misago:admin:settings:general:index"),
            {
                "forum_name": "Misago",
                "forum_address": "http://test.com",
                "logo": not_image,
            },
        )

    setting.refresh_from_db()
    assert not setting.image


def test_uploading_invalid_file_doesnt_remove_already_set_image(
    admin_client, setting_with_value
):
    with open(OTHER_FILE, "rb") as not_image:
        admin_client.post(
            reverse("misago:admin:settings:general:index"),
            {
                "forum_name": "Misago",
                "forum_address": "http://test.com",
                "logo": not_image,
            },
        )

    setting_with_value.refresh_from_db()
    assert setting_with_value.image


def test_set_image_is_still_rendered_when_invalid_file_was_uploaded(
    admin_client, setting_with_value
):
    with open(OTHER_FILE, "rb") as not_image:
        response = admin_client.post(
            reverse("misago:admin:settings:general:index"),
            {
                "forum_name": "Misago",
                "forum_address": "http://test.com",
                "logo": not_image,
            },
        )

    assert_contains(response, setting_with_value.image.url)


def test_uploading_new_image_replaces_already_set_image(
    admin_client, setting_with_value
):
    with open(OTHER_IMAGE, "rb") as not_image:
        admin_client.post(
            reverse("misago:admin:settings:general:index"),
            {
                "forum_name": "Misago",
                "forum_address": "http://test.com",
                "logo": not_image,
            },
        )

    setting_with_value.refresh_from_db()
    assert str(setting_with_value.image.name).endswith(".d18644ab.png")


def test_uploading_new_image_deletes_image_file(admin_client, setting_with_value):
    with open(OTHER_IMAGE, "rb") as not_image:
        admin_client.post(
            reverse("misago:admin:settings:general:index"),
            {
                "forum_name": "Misago",
                "forum_address": "http://test.com",
                "logo": not_image,
            },
        )

    assert not os.path.exists(setting_with_value.image.path)


def test_omitting_setting_value_doesnt_remove_already_set_image(
    admin_client, setting_with_value
):
    admin_client.post(
        reverse("misago:admin:settings:general:index"),
        {"forum_name": "Misago", "forum_address": "http://test.com"},
    )

    setting_with_value.refresh_from_db()
    assert setting_with_value.image


def test_set_image_can_be_deleted_by_extra_option(admin_client, setting_with_value):
    admin_client.post(
        reverse("misago:admin:settings:general:index"),
        {"forum_name": "Misago", "forum_address": "http://test.com", "logo_delete": 1},
    )

    setting_with_value.refresh_from_db()
    assert not setting_with_value.image


def test_using_image_deletion_option_deletes_image_file(
    admin_client, setting_with_value
):
    admin_client.post(
        reverse("misago:admin:settings:general:index"),
        {"forum_name": "Misago", "forum_address": "http://test.com", "logo_delete": 1},
    )

    assert not os.path.exists(setting_with_value.image.path)
