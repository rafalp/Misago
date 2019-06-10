from ....test import assert_contains


def test_icons_admin_view_displays(admin_client, admin_link):
    response = admin_client.get(admin_link)
    assert response.status_code == 200


def test_set_favicon_displays(admin_client, admin_link, favicon):
    response = admin_client.get(admin_link)
    assert_contains(response, favicon.image.url)


def test_set_favicon_32_displays(admin_client, admin_link, favicon_32):
    response = admin_client.get(admin_link)
    assert_contains(response, favicon_32.image.url)


def test_set_favicon_16_displays(admin_client, admin_link, favicon_16):
    response = admin_client.get(admin_link)
    assert_contains(response, favicon_16.image.url)


def test_set_apple_touch_icon_displays(admin_client, admin_link, apple_touch_icon):
    response = admin_client.get(admin_link)
    assert_contains(response, apple_touch_icon.image.url)
