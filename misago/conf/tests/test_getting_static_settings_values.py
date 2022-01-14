import pytest

from ..staticsettings import StaticSettings


def mock_settings(settings):
    mocks = {
        "MISAGO_DATABASE_URL": "mock",
        "MISAGO_CACHE_URL": "mock",
        "MISAGO_PUBSUB_URL": "mock",
        "MISAGO_STATIC_ROOT": "mock",
        "MISAGO_MEDIA_ROOT": "mock",
    }
    mocks.update(settings)
    return mocks


def test_debug_setting_value_is_set_and_retrieved():
    settings = StaticSettings(mock_settings({"MISAGO_DEBUG": "true"}))
    assert settings.debug is True


def test_debug_setting_value_is_set_to_false():
    settings = StaticSettings(mock_settings({"MISAGO_DEBUG": "false"}))
    assert settings.debug is False


def test_debug_setting_value_defaults_to_false():
    settings = StaticSettings(mock_settings({}))
    assert settings.debug is False


def test_test_setting_value_is_set_and_retrieved():
    settings = StaticSettings(mock_settings({"MISAGO_TEST": "true"}))
    assert settings.test is True


def test_test_setting_value_is_set_to_false():
    settings = StaticSettings(mock_settings({"MISAGO_TEST": "false"}))
    assert settings.test is False


def test_test_setting_value_defaults_to_false():
    settings = StaticSettings(mock_settings({}))
    assert settings.test is False


def test_test_database_url_setting_value_is_set_and_retrieved():
    settings = StaticSettings(mock_settings({"MISAGO_TEST_DATABASE_NAME": "test_db"}))
    assert settings.test_database_name == "test_db"


def test_database_url_setting_value_is_set_and_retrieved():
    settings = StaticSettings(mock_settings({"MISAGO_DATABASE_URL": "/database-test/"}))
    assert settings.database_url == "/database-test/"


def test_cache_url_setting_value_is_set_and_retrieved():
    settings = StaticSettings(mock_settings({"MISAGO_CACHE_URL": "/cache-test/"}))
    assert settings.cache_url == "/cache-test/"


def test_pubsub_url_setting_value_is_set_and_retrieved():
    settings = StaticSettings(mock_settings({"MISAGO_PUBSUB_URL": "/pubsub-test/"}))
    assert settings.pubsub_url == "/pubsub-test/"


def test_static_root_setting_value_is_set_and_retrieved():
    settings = StaticSettings(mock_settings({"MISAGO_STATIC_ROOT": "/static-test/"}))
    assert settings.static_root == "/static-test/"


def test_media_root_setting_value_is_set_and_retrieved():
    settings = StaticSettings(mock_settings({"MISAGO_MEDIA_ROOT": "/media-test/"}))
    assert settings.media_root == "/media-test/"


def test_media_url_setting_value_is_set_and_retrieved():
    settings = StaticSettings(mock_settings({"MISAGO_MEDIA_URL": "/media-url-test/"}))
    assert settings.media_url == "/media-url-test/"


def test_media_url_setting_value_is_normalized_when_set():
    settings = StaticSettings(mock_settings({"MISAGO_MEDIA_URL": "/ media-dirty  "}))
    assert settings.media_url == "/media-dirty/"


def test_media_url_setting_value_is_set_to_default_value_if_not_set():
    settings = StaticSettings(mock_settings({}))
    assert settings.media_url == "/media/"


def test_plugins_root_setting_value_is_set_and_retrieved():
    settings = StaticSettings(mock_settings({"MISAGO_PLUGINS_ROOT": "/plugins-test/"}))
    assert settings.plugins_root == "/plugins-test/"


def test_avatar_sizes_setting_value_is_set_and_retrieved():
    settings = StaticSettings(
        mock_settings({"MISAGO_AVATAR_SIZES": "20 , 40 ,40, 100"})
    )
    assert settings.avatar_sizes == [100, 40, 20]


def test_avatar_sizes_setting_value_is_validated():
    with pytest.raises(ValueError):
        StaticSettings(mock_settings({"MISAGO_AVATAR_SIZES": "20 , invalid , 100"}))
