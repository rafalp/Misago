from ...test import assert_contains


def test_favicon_html_is_present_in_html_if_set(user_client, favicon):
    response = user_client.get("/")
    assert_contains(response, favicon.image.url)


def test_favicon_32_html_is_present_in_html_if_set(user_client, favicon_32):
    response = user_client.get("/")
    assert_contains(response, favicon_32.image.url)


def test_favicon_16_html_is_present_in_html_if_set(user_client, favicon_16):
    response = user_client.get("/")
    assert_contains(response, favicon_16.image.url)


def test_apple_touch_icon_html_is_present_in_html_if_set(user_client, apple_touch_icon):
    response = user_client.get("/")
    assert_contains(response, apple_touch_icon.image.url)
