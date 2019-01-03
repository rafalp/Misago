import pytest
from django.urls import reverse

from ....test import assert_has_success_message


@pytest.fixture
def delete_css(admin_client):
    def delete_assets(theme, assets):
        url = reverse(
            "misago:admin:appearance:themes:delete-css", kwargs={"pk": theme.pk}
        )
        return admin_client.post(url, {"item": [i.pk for i in assets]})

    return delete_assets


@pytest.fixture
def delete_media(admin_client):
    def delete_assets(theme, assets):
        url = reverse(
            "misago:admin:appearance:themes:delete-media", kwargs={"pk": theme.pk}
        )
        return admin_client.post(url, {"item": [i.pk for i in assets]})

    return delete_assets


def test_theme_css_can_be_deleted(theme, delete_css, css):
    delete_css(theme, [css])
    assert not theme.css.exists()


def test_theme_css_link_can_be_deleted(theme, delete_css, css_link):
    delete_css(theme, [css_link])
    assert not theme.css.exists()


def test_multiple_theme_css_can_be_deleted_at_single_time(
    theme, delete_css, css, css_link
):
    delete_css(theme, [css, css_link])
    assert not theme.css.exists()


def test_theme_media_can_be_deleted(theme, delete_media, media):
    delete_media(theme, [media])
    assert not theme.media.exists()


def test_theme_images_can_be_deleted(theme, delete_media, image):
    delete_media(theme, [image])
    assert not theme.media.exists()


def test_multiple_theme_media_can_be_deleted_at_single_time(
    theme, delete_media, media, image
):
    delete_media(theme, [media, image])
    assert not theme.media.exists()


def test_success_message_is_set_after_css_is_deleted(theme, delete_css, css):
    response = delete_css(theme, [css])
    assert_has_success_message(response)


def test_success_message_is_set_after_media_is_deleted(theme, delete_media, media):
    response = delete_media(theme, [media])
    assert_has_success_message(response)


def test_selecting_no_css_to_delete_causes_no_errors(theme, delete_css, css):
    delete_css(theme, [])
    assert theme.css.exists()


def test_selecting_no_media_to_delete_causes_no_errors(theme, delete_media, media):
    delete_media(theme, [])
    assert theme.media.exists()


def test_selecting_invalid_css_id_to_delete_causes_no_errors(
    mocker, theme, delete_css, css
):
    delete_css(theme, [mocker.Mock(pk="str")])
    assert theme.css.exists()


def test_selecting_invalid_media_id_to_delete_causes_no_errors(
    mocker, theme, delete_media, media
):
    delete_media(theme, [mocker.Mock(pk="str")])
    assert theme.media.exists()


def test_selecting_nonexisting_css_id_to_delete_causes_no_errors(
    mocker, theme, delete_css, css
):
    delete_css(theme, [mocker.Mock(pk=css.pk + 1)])
    assert theme.css.exists()


def test_selecting_nonexisting_media_id_to_delete_causes_no_errors(
    mocker, theme, delete_media, media
):
    delete_media(theme, [mocker.Mock(pk=media.pk + 1)])
    assert theme.media.exists()


def test_other_theme_css_is_not_deleted(delete_css, theme, other_theme, css):
    delete_css(other_theme, [css])
    assert theme.css.exists()


def test_other_theme_media_is_not_deleted(delete_media, theme, other_theme, media):
    delete_media(other_theme, [media])
    assert theme.media.exists()
