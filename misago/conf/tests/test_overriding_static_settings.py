import pytest

from ..test import override_static_settings


def test_static_setting_can_be_overridden_using_context_manager(static_settings):
    assert static_settings.CUSTOM_SETTING == "misago"
    with override_static_settings(CUSTOM_SETTING="overrided"):
        assert static_settings.CUSTOM_SETTING == "overrided"
    assert static_settings.CUSTOM_SETTING == "misago"


def test_static_setting_can_be_overridden_using_decorator(static_settings):
    @override_static_settings(CUSTOM_SETTING="overrided")
    def decorated_function():
        return static_settings.CUSTOM_SETTING

    assert static_settings.CUSTOM_SETTING == "misago"
    assert decorated_function() == "overrided"
    assert static_settings.CUSTOM_SETTING == "misago"


def test_nonexistant_setting_can_be_set_using_context_manager(static_settings):
    with pytest.raises(AttributeError):
        static_settings.NONEXISTANT_SETTING  # pylint: disable=pointless-statement

    with override_static_settings(NONEXISTANT_SETTING="set"):
        assert static_settings.NONEXISTANT_SETTING == "set"

    with pytest.raises(AttributeError):
        static_settings.NONEXISTANT_SETTING  # pylint: disable=pointless-statement


def test_nonexistant_setting_can_be_set_using_decorator(static_settings):
    @override_static_settings(NONEXISTANT_SETTING="set")
    def decorated_function():
        return static_settings.NONEXISTANT_SETTING

    with pytest.raises(AttributeError):
        static_settings.NONEXISTANT_SETTING  # pylint: disable=pointless-statement

    assert decorated_function() == "set"

    with pytest.raises(AttributeError):
        static_settings.NONEXISTANT_SETTING  # pylint: disable=pointless-statement
