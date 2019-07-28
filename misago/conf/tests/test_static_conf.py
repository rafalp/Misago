import pytest

from ..static import StaticConf


def test_static_conf_setup_loads_settings_from_specified_python_path():
    conf = StaticConf()
    conf.setup("misago.conf.tests.settings")
    assert conf.DEBUG is True


def test_static_conf_setup_raises_import_error_when_invalid_path_is_given():
    conf = StaticConf()
    with pytest.raises(ImportError):
        conf.setup("misago.invalid")


def test_unconfigured_static_conf_raises_error_when_setting_is_accessed():
    conf = StaticConf()
    with pytest.raises(AssertionError):
        conf.DEBUG  # pylint: disable=pointless-statement
