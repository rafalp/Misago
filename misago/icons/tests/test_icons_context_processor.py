from ..context_processors import icons
from ..models import Icon


def test_context_processor_adds_icons_key_to_context(db):
    assert "icons" in icons(None)


def test_icons_context_defaults_to_empty_dict(db):
    assert icons(None) == {"icons": {}}


def test_set_favicon_icon_is_present_in_context(favicon):
    assert Icon.TYPE_FAVICON in icons(None)["icons"]


def test_set_favicon_32_icon_is_present_in_context(favicon_32):
    assert Icon.TYPE_FAVICON_32 in icons(None)["icons"]


def test_set_favicon_16_icon_is_present_in_context(favicon_16):
    assert Icon.TYPE_FAVICON_16 in icons(None)["icons"]


def test_set_apple_touch_icon_icon_is_present_in_context(apple_touch_icon):
    assert Icon.TYPE_APPLE_TOUCH_ICON in icons(None)["icons"]
