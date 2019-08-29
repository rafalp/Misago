from ..staticsettings import StaticSettings


def test_debug_setting_value_is_set_and_retrieved():
    settings = StaticSettings({"MISAGO_DEBUG": "true"})
    assert settings.debug is True


def test_debug_setting_value_is_set_to_false():
    settings = StaticSettings({"MISAGO_DEBUG": "false"})
    assert settings.debug is False


def test_debug_setting_value_defaults_to_false():
    settings = StaticSettings({})
    assert settings.debug is False


def test_test_setting_value_is_set_and_retrieved():
    settings = StaticSettings({"MISAGO_TEST": "true"})
    assert settings.test is True


def test_test_setting_value_is_set_to_false():
    settings = StaticSettings({"MISAGO_TEST": "false"})
    assert settings.test is False


def test_test_setting_value_defaults_to_false():
    settings = StaticSettings({})
    assert settings.test is False


def test_database_url_setting_value_is_set_and_retrieved():
    settings = StaticSettings({"MISAGO_DATABASE_URL": "/database-test/"})
    assert settings.database_url == "/database-test/"


def test_cache_url_setting_value_is_set_and_retrieved():
    settings = StaticSettings({"MISAGO_CACHE_URL": "/cache-test/"})
    assert settings.cache_url == "/cache-test/"


def test_static_root_url_setting_value_is_set_and_retrieved():
    settings = StaticSettings({"MISAGO_STATIC_ROOT": "/static-test/"})
    assert settings.static_root == "/static-test/"


def test_media_root_url_setting_value_is_set_and_retrieved():
    settings = StaticSettings({"MISAGO_MEDIA_ROOT": "/media-test/"})
    assert settings.media_root == "/media-test/"


def test_plugins_setting_value_is_set_and_retrieved():
    settings = StaticSettings({"MISAGO_PLUGINS": "/plugins-test/"})
    assert settings.plugins == "/plugins-test/"
