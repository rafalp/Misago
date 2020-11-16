import pytest
from django.urls import reverse

from ....test import assert_contains, assert_not_contains, assert_has_error_message


@pytest.fixture
def assets_client(admin_client):
    def get_theme_assets(theme):
        url = reverse("misago:admin:themes:assets", kwargs={"pk": theme.pk})
        return admin_client.get(url)

    return get_theme_assets


def test_theme_assets_list_is_displayed(assets_client, theme):
    response = assets_client(theme)
    assert_contains(response, theme.name)


def test_css_file_is_displayed_on_theme_asset_list(assets_client, theme, css):
    response = assets_client(theme)
    assert_contains(response, css.name)


def test_css_link_is_displayed_on_theme_asset_list(assets_client, theme, css_link):
    response = assets_client(theme)
    assert_contains(response, css_link.name)


def test_media_is_displayed_on_themes_asset_list(assets_client, theme, media):
    response = assets_client(theme)
    assert_contains(response, media.name)


def test_image_is_displayed_on_themes_asset_list(assets_client, theme, image):
    response = assets_client(theme)
    assert_contains(response, image.name)


def test_image_thumbnail_is_displayed_on_themes_asset_list(assets_client, theme, image):
    response = assets_client(theme)
    assert_contains(response, image.thumbnail.url)


def test_other_theme_assets_are_not_displayed(
    assets_client, other_theme, css, css_link, media, image
):
    response = assets_client(other_theme)
    assert_not_contains(response, css.name)
    assert_not_contains(response, css_link.name)
    assert_not_contains(response, media.name)
    assert_not_contains(response, image.name)


def test_user_is_redirected_away_with_message_from_default_theme_assets_list(
    assets_client, default_theme
):
    response = assets_client(default_theme)
    assert response.status_code == 302
    assert_has_error_message(response)


def test_user_is_redirected_away_with_message_from_nonexisting_theme(
    assets_client, nonexisting_theme
):
    response = assets_client(nonexisting_theme)
    assert response.status_code == 302
    assert_has_error_message(response)
