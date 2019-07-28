import pytest

from ..static import StaticConf


def test_unconfigured_static_conf_raises_error_when_setting_is_accessed():
    conf = StaticConf()
    with pytest.raises(AssertionError):
        assert conf.DEBUG
