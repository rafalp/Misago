import pytest

from .conf.cache import SETTINGS_CACHE
from .conf.dynamicsettings import get_dynamic_settings
from .database import database
from .database.testdatabase import create_test_database, teardown_test_database


def pytest_configure():
    create_test_database()


def pytest_unconfigure():
    teardown_test_database()


@pytest.fixture(scope="function")
async def db():
    async with database:
        yield


@pytest.fixture
def cache_versions():
    return {SETTINGS_CACHE: "settings-cache"}


@pytest.fixture
async def dynamic_settings(db, cache_versions):
    return await get_dynamic_settings(cache_versions)
