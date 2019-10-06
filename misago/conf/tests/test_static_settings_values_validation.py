import pytest

from ..staticsettings import StaticSettings, get_setting_value


@pytest.fixture
def mock_settings():
    return {
        "MISAGO_DATABASE_URL": "mock",
        "MISAGO_CACHE_URL": "mock",
        "MISAGO_STATIC_ROOT": "mock",
        "MISAGO_MEDIA_ROOT": "mock",
    }


def test_setting_value_is_returned_if_its_set():
    assert get_setting_value({"setting": "value"}, "setting") == "value"


def test_value_error_is_raised_if_setting_is_not_set():
    with pytest.raises(ValueError):
        assert get_setting_value({"setting": "value"}, "nonexisting_setting")


def test_value_error_is_raised_if_setting_is_empty():
    with pytest.raises(ValueError):
        assert get_setting_value({"setting": ""}, "setting")


def test_value_error_is_raised_if_database_url_is_not_set(mock_settings):
    mock_settings.pop("MISAGO_DATABASE_URL")
    with pytest.raises(ValueError):
        StaticSettings(mock_settings)


def test_value_error_is_raised_if_database_url_is_empty(mock_settings):
    mock_settings["MISAGO_DATABASE_URL"] = ""
    with pytest.raises(ValueError):
        StaticSettings(mock_settings)


def test_value_error_is_raised_if_cache_url_is_not_set(mock_settings):
    mock_settings.pop("MISAGO_CACHE_URL")
    with pytest.raises(ValueError):
        StaticSettings(mock_settings)


def test_value_error_is_raised_if_cache_url_is_empty(mock_settings):
    mock_settings["MISAGO_CACHE_URL"] = ""
    with pytest.raises(ValueError):
        StaticSettings(mock_settings)


def test_value_error_is_raised_if_static_root_is_not_set(mock_settings):
    mock_settings.pop("MISAGO_STATIC_ROOT")
    with pytest.raises(ValueError):
        StaticSettings(mock_settings)


def test_value_error_is_raised_if_static_root_is_empty(mock_settings):
    mock_settings["MISAGO_STATIC_ROOT"] = ""
    with pytest.raises(ValueError):
        StaticSettings(mock_settings)


def test_value_error_is_raised_if_media_root_is_not_set(mock_settings):
    mock_settings.pop("MISAGO_MEDIA_ROOT")
    with pytest.raises(ValueError):
        StaticSettings(mock_settings)


def test_value_error_is_raised_if_media_root_is_empty(mock_settings):
    mock_settings["MISAGO_MEDIA_ROOT"] = ""
    with pytest.raises(ValueError):
        StaticSettings(mock_settings)
