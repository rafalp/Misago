import pytest

from .conf.cache import SETTINGS_CACHE
from .conf.dynamicsettings import get_dynamic_settings
from .database import database
from .database.testdatabase import create_test_database, teardown_test_database
from .users.create import create_user


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


@pytest.fixture
async def user_password():
    return "t3st+p4ssw0rd!"


@pytest.fixture
async def user(db, user_password):
    return await create_user("User", "user@example.com", password=user_password)
