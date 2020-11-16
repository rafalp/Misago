from ..dynamicsettings import DynamicSettings
from ..test import override_dynamic_settings


def test_dynamic_setting_can_be_overridden_using_context_manager(dynamic_settings):
    assert dynamic_settings.forum_name == "Misago"
    with override_dynamic_settings(forum_name="Overrided"):
        assert dynamic_settings.forum_name == "Overrided"
    assert dynamic_settings.forum_name == "Misago"


def test_dynamic_setting_can_be_overridden_using_decorator(dynamic_settings):
    @override_dynamic_settings(forum_name="Overrided")
    def decorated_function(settings):
        return settings.forum_name

    assert dynamic_settings.forum_name == "Misago"
    assert decorated_function(dynamic_settings) == "Overrided"
    assert dynamic_settings.forum_name == "Misago"


def test_lazy_dynamic_setting_can_be_overridden_using_context_manager(
    cache_versions, lazy_setting
):
    settings = DynamicSettings(cache_versions)
    assert settings.get_lazy_setting_value("lazy_setting") == "Hello"
    with override_dynamic_settings(lazy_setting="Overrided"):
        assert settings.get_lazy_setting_value("lazy_setting") == "Overrided"
    assert settings.get_lazy_setting_value("lazy_setting") == "Hello"


def test_lazy_dynamic_setting_can_be_overridden_using_decorator(
    cache_versions, lazy_setting
):
    @override_dynamic_settings(lazy_setting="Overrided")
    def decorated_function(settings):
        return settings.get_lazy_setting_value("lazy_setting")

    settings = DynamicSettings(cache_versions)
    assert settings.get_lazy_setting_value("lazy_setting") == "Hello"
    assert decorated_function(settings) == "Overrided"
    assert settings.get_lazy_setting_value("lazy_setting") == "Hello"
