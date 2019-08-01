import pytest

from ..staticsettings import StaticSettings


@pytest.fixture
def static_settings():
    settings = StaticSettings()
    settings.setup("misago.conf.tests.settings")
    return settings
