import pytest

from ..staticsettings import StaticSettings


def test_static_settings_setup_loads_settings_from_specified_python_path():
    settings = StaticSettings()
    settings.setup("misago.conf.tests.settings")
    assert settings.DEBUG is True


def test_static_settings_setup_raises_error_when_no_path_is_given():
    settings = StaticSettings()
    with pytest.raises(AssertionError):
        settings.setup(None)


def test_static_settings_setup_raises_error_when_empty_path_is_given():
    settings = StaticSettings()
    with pytest.raises(AssertionError):
        settings.setup("")


def test_static_settings_setup_raises_error_if_it_is_called_more_than_once():
    settings = StaticSettings()
    settings.setup("misago.conf.tests.settings")
    with pytest.raises(AssertionError):
        settings.setup("misago.conf.tests.settings")


def test_static_settings_setup_raises_import_error_when_invalid_path_is_given():
    settings = StaticSettings()
    with pytest.raises(ImportError):
        settings.setup("misago.invalid")


def test_static_settings_raises_error_when_setting_is_accessed_before_setup():
    settings = StaticSettings()
    with pytest.raises(AssertionError):
        settings.DEBUG  # pylint: disable=pointless-statement
