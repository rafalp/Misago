import pytest

from ..staticsettings import StaticSettings


def test_default_setting_value_is_resolved(static_settings):
    assert static_settings.INSTALLED_PLUGINS == []


def test_custom_setting_value_is_resolved(static_settings):
    assert static_settings.CUSTOM_SETTING == "misago"


def test_error_is_raised_when_undefined_setting_is_accessed(static_settings):
    with pytest.raises(AttributeError):
        assert static_settings.UNDEFINED_ERROR


def test_lower_case_names_in_module_are_not_imported_as_settings(static_settings):
    with pytest.raises(AttributeError):
        assert static_settings.lowercase_value  # pylint: disable=pointless-statement


def test_static_settings_raises_error_when_setting_is_accessed_before_setup():
    settings = StaticSettings()
    with pytest.raises(AssertionError):
        settings.DEBUG  # pylint: disable=pointless-statement
