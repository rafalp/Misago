from django.test import TestCase, override_settings

from misago.conf.staticsettings import StaticSettings


class GettingSettingValueTests(TestCase):
    def test_accessing_attr_returns_setting_value_defined_in_settings_file(self):
        settings = StaticSettings()
        assert settings.STATIC_URL

    def test_accessing_attr_returns_setting_value_defined_in_misago_defaults_file(self):
        settings = StaticSettings()
        assert settings.MISAGO_MOMENT_JS_LOCALES

    def test_setting_value_can_be_overridden_using_django_util(self):
        settings = StaticSettings()
        with override_settings(STATIC_URL="/test/"):
            assert settings.STATIC_URL == "/test/"

    def test_default_setting_value_can_be_overridden_using_django_util(self):
        settings = StaticSettings()
        with override_settings(MISAGO_MOMENT_JS_LOCALES="test"):
            assert settings.MISAGO_MOMENT_JS_LOCALES == "test"

    def test_undefined_setting_value_can_be_overridden_using_django_util(self):
        settings = StaticSettings()
        with override_settings(UNDEFINED_SETTING="test"):
            assert settings.UNDEFINED_SETTING == "test"