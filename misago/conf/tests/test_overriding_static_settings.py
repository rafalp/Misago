import pytest

from ..staticsettings import StaticSettings
from ..test import override_static_settings


@pytest.fixture
def settings():
    return StaticSettings(
        {
            "MISAGO_DEBUG": "true",
            "MISAGO_TEST": "true",
            "MISAGO_DATABASE_URL": "database",
            "MISAGO_CACHE_URL": "cache",
            "MISAGO_STATIC_ROOT": "static_root",
            "MISAGO_MEDIA_ROOT": "media_root",
            "MISAGO_PLUGINS": "plugins",
        }
    )


def test_static_setting_can_be_overridden_using_context_manager(settings):
    assert settings.debug is True
    with override_static_settings(debug=False):
        assert settings.debug is False
    assert settings.debug is True


def test_static_setting_can_be_overridden_using_decorator(settings):
    @override_static_settings(debug=False)
    def decorated_function():
        return settings.debug

    assert settings.debug is True
    assert decorated_function() is False
    assert settings.debug is True


def test_overriding_test_setting_using_context_manager_raises_error(settings):
    with pytest.raises(AssertionError):
        with override_static_settings(test=False):
            pass


def test_overriding_test_setting_using_decorator_raises_error(settings):
    @override_static_settings(test=False)
    def decorated_function():
        pass

    with pytest.raises(AssertionError):
        decorated_function()


def test_overriding_nonexistant_setting_using_context_manager_raises_error(settings):
    with pytest.raises(AssertionError):
        with override_static_settings(nonexistant_setting=True):
            pass


def test_overriding_nonexistant_setting_using_decorator_raises_error(settings):
    @override_static_settings(nonexistant_setting=True)
    def decorated_function():
        pass

    with pytest.raises(AssertionError):
        decorated_function()


def test_database_url_setting_can_be_overridden(settings):
    with override_static_settings(database_url="overridded"):
        assert settings.database_url == "overridded"


def test_cache_url_setting_can_be_overridden(settings):
    with override_static_settings(cache_url="overridded"):
        assert settings.cache_url == "overridded"


def test_static_root_setting_can_be_overridden(settings):
    with override_static_settings(static_root="overridded"):
        assert settings.static_root == "overridded"


def test_media_root_setting_can_be_overridden(settings):
    with override_static_settings(media_root="overridded"):
        assert settings.media_root == "overridded"


def test_plugins_setting_can_be_overridden(settings):
    with override_static_settings(plugins="overridded"):
        assert settings.plugins == "overridded"
