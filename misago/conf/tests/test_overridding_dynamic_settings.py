from django.test import TestCase

from misago.conf import SETTINGS_CACHE
from misago.conf.dynamicsettings import DynamicSettings
from misago.conf.models import Setting, SettingsGroup
from misago.conftest import get_cache_versions

from misago.conf.test import override_dynamic_settings

cache_versions = get_cache_versions()


class OverrideDynamicSettingsTests(TestCase):
    def test_dynamic_setting_can_be_overridden_using_context_manager(self):
        settings = DynamicSettings(cache_versions)
        assert settings.forum_name == "Misago"

        with override_dynamic_settings(forum_name="Overrided"):
            assert settings.forum_name == "Overrided"

        assert settings.forum_name == "Misago"

    def test_dynamic_setting_can_be_overridden_using_decorator(self):
        @override_dynamic_settings(forum_name="Overrided")
        def decorated_function(settings):
            return settings.forum_name

        settings = DynamicSettings(cache_versions)
        assert settings.forum_name == "Misago"
        assert decorated_function(settings) == "Overrided"
        assert settings.forum_name == "Misago"

    def test_lazy_dynamic_setting_can_be_overridden_using_context_manager(self):
        settings_group = SettingsGroup.objects.create(key="test", name="Test")
        setting = Setting.objects.create(
            group=settings_group,
            setting="lazy_setting",
            name="Lazy setting",
            dry_value="Hello",
            is_lazy=True,
            field_extra={},
        )

        settings = DynamicSettings(cache_versions)
        assert settings.get_lazy_setting_value("lazy_setting") == "Hello"
        with override_dynamic_settings(lazy_setting="Overrided"):
            assert settings.get_lazy_setting_value("lazy_setting") == "Overrided"
        assert settings.get_lazy_setting_value("lazy_setting") == "Hello"

    def test_lazy_dynamic_setting_can_be_overridden_using_decorator(self):
        @override_dynamic_settings(lazy_setting="Overrided")
        def decorated_function(settings):
            return settings.get_lazy_setting_value("lazy_setting")

        settings_group = SettingsGroup.objects.create(key="test", name="Test")
        setting = Setting.objects.create(
            group=settings_group,
            setting="lazy_setting",
            name="Lazy setting",
            dry_value="Hello",
            is_lazy=True,
            field_extra={},
        )
        
        settings = DynamicSettings(cache_versions)
        assert settings.get_lazy_setting_value("lazy_setting") == "Hello"
        assert decorated_function(settings) == "Overrided"
        assert settings.get_lazy_setting_value("lazy_setting") == "Hello"
