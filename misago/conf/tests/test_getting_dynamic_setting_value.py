from unittest.mock import patch

from django.test import TestCase

from misago.conf import CACHE_NAME
from misago.conf.dynamicsettings import DynamicSettings
from misago.conf.models import Setting, SettingsGroup

from . import override_dynamic_settings

cache_versions = {CACHE_NAME: "abcdefgh"}


class GettingSettingValueTests(TestCase):
    @patch('django.core.cache.cache.set')
    @patch('django.core.cache.cache.get', return_value=None)
    def test_dynamic_settings_are_loaded_from_database_if_cache_is_not_available(self, cache_get, _):
        with self.assertNumQueries(1):
            DynamicSettings(cache_versions)

    @patch('django.core.cache.cache.set')
    @patch('django.core.cache.cache.get', return_value={})
    def test_dynamic_settings_are_loaded_from_cache_if_it_is_not_none(self, cache_get, _):
        with self.assertNumQueries(0):
            DynamicSettings(cache_versions)
        cache_get.assert_called_once()

    @patch('django.core.cache.cache.set')
    @patch('django.core.cache.cache.get', return_value=None)
    def test_dynamic_settings_cache_is_set_if_none_exists(self, _, cache_set):
        DynamicSettings(cache_versions)
        cache_set.assert_called_once()

    @patch('django.core.cache.cache.set')
    @patch('django.core.cache.cache.get', return_value={})
    def test_dynamic_settings_cache_is_not_set_if_it_already_exists(self, _, cache_set):
        with self.assertNumQueries(0):
            DynamicSettings(cache_versions)
        cache_set.assert_not_called()

    def test_accessing_attr_returns_setting_value(self):
        settings = DynamicSettings(cache_versions)
        assert settings.forum_name == "Misago"

    def test_accessing_attr_for_undefined_setting_raises_error(self):
        settings = DynamicSettings(cache_versions)
        with self.assertRaises(KeyError):
            settings.not_existing

    def test_accessing_attr_for_lazy_setting_without_value_returns_none(self):
        settings_group = SettingsGroup.objects.create(key="test", name="Test")
        setting = Setting.objects.create(
            group=settings_group,
            setting="lazy_setting",
            name="Lazy setting",
            is_lazy=True,
            field_extra={},
        )

        settings = DynamicSettings(cache_versions)
        assert settings.lazy_setting is None

    def test_accessing_attr_for_lazy_setting_with_value_returns_true(self):
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
        assert settings.lazy_setting is True

    def test_lazy_setting_getter_for_lazy_setting_with_value_returns_real_value(self):
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

    def test_lazy_setting_getter_for_lazy_setting_makes_db_query(self):
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
        with self.assertNumQueries(1):
            settings.get_lazy_setting_value("lazy_setting")

    def test_lazy_setting_getter_for_lazy_setting_is_reusing_query_result(self):
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
        settings.get_lazy_setting_value("lazy_setting")
        with self.assertNumQueries(0):
            settings.get_lazy_setting_value("lazy_setting")

    def test_lazy_setting_getter_for_undefined_setting_raises_attribute_error(self):
        settings = DynamicSettings(cache_versions)
        with self.assertRaises(AttributeError):
            settings.get_lazy_setting_value("undefined")

    def test_lazy_setting_getter_for_not_lazy_setting_raises_value_error(self):
        settings = DynamicSettings(cache_versions)
        with self.assertRaises(ValueError):
            settings.get_lazy_setting_value("forum_name")