import pytest
from django.test import override_settings


def test_accessing_attr_returns_setting_value_defined_in_settings_file(settings):
    assert settings.STATIC_URL


def test_accessing_attr_returns_setting_value_defined_in_misago_defaults_file(settings):
    assert settings.MISAGO_MOMENT_JS_LOCALES


def test_setting_value_can_be_overridden_using_django_util(settings):
    with override_settings(STATIC_URL="/test/"):
        assert settings.STATIC_URL == "/test/"


def test_default_setting_value_can_be_overridden_using_django_util(settings):
    with override_settings(MISAGO_MOMENT_JS_LOCALES="test"):
        assert settings.MISAGO_MOMENT_JS_LOCALES == "test"


def test_undefined_setting_value_can_be_overridden_using_django_util(settings):
    with override_settings(UNDEFINED_SETTING="test"):
        assert settings.UNDEFINED_SETTING == "test"


def test_accessing_attr_for_undefined_setting_raises_attribute_error(settings):
    with pytest.raises(AttributeError):
        assert settings.UNDEFINED_SETTING
