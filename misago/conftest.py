from unittest.mock import Mock

import pytest

from . import tables
from .conf.cache import SETTINGS_CACHE
from .conf.dynamicsettings import get_dynamic_settings
from .database import database
from .database.queries import insert
from .database.testdatabase import create_test_database, teardown_test_database
from .graphql.context import get_graphql_context
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
async def cache_version(db):
    await insert(tables.cache_versions, cache="test_cache", version="version")
    return {"cache": "test_cache", "version": "version"}


@pytest.fixture
async def other_cache_version(db):
    await insert(tables.cache_versions, cache="test_other_cache", version="version")
    return {"cache": "test_other_cache", "version": "version"}


@pytest.fixture
async def dynamic_settings(db, cache_versions):
    return await get_dynamic_settings(cache_versions)


@pytest.fixture
async def user_password():
    return "t3st+p4ssw0rd!"


@pytest.fixture
async def user(db, user_password):
    return await create_user("User", "user@example.com", password=user_password)


@pytest.fixture
async def other_user(db, user_password):
    return await create_user(
        "OtherUser", "other-user@example.com", password=user_password
    )


@pytest.fixture
async def deactivated_user(db, user_password):
    return await create_user(
        "User", "user@example.com", password=user_password, is_deactivated=True
    )


@pytest.fixture
async def no_password_user(db):
    return await create_user("NopassUser", "nopass-user@example.com")


@pytest.fixture
async def graphql_context(db):
    return await get_graphql_context(None)


@pytest.fixture
def graphql_info(graphql_context):
    return Mock(context=graphql_context)
