from unittest.mock import Mock

import pytest

from . import tables
from .categories.create import create_category
from .conf.cache import SETTINGS_CACHE
from .conf.dynamicsettings import get_dynamic_settings
from .database import database
from .database.queries import insert
from .database.testdatabase import create_test_database, teardown_test_database
from .threads.create import create_post, create_thread
from .threads.update import update_thread
from .users.create import create_user


def pytest_configure():
    create_test_database()


def pytest_unconfigure():
    teardown_test_database()


@pytest.fixture
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
async def categories(db):
    top_category = await create_category(name="Category", left=7, right=10)
    child_category = await create_category(
        name="Child Category", parent=top_category, left=8, right=9, depth=1
    )
    sibling_category = await create_category(name="Sibling Category", left=11, right=12)
    closed_category = await create_category(
        name="Closed Category", left=13, right=14, is_closed=True
    )
    return (top_category, child_category, sibling_category, closed_category)


@pytest.fixture
def category(categories):
    return categories[0]


@pytest.fixture
def child_category(categories):
    return categories[1]


@pytest.fixture
def sibling_category(categories):
    return categories[2]


@pytest.fixture
def closed_category(categories):
    return categories[3]


@pytest.fixture
def user_password():
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
def graphql_context(cache_versions, dynamic_settings):
    return {
        "request": Mock(headers={}),
        "cache_versions": cache_versions,
        "settings": dynamic_settings,
    }


@pytest.fixture
def graphql_info(graphql_context):
    return Mock(context=graphql_context)


@pytest.fixture
def user_graphql_context(cache_versions, dynamic_settings, user):
    return {
        "request": Mock(headers={}),
        "cache_versions": cache_versions,
        "settings": dynamic_settings,
        "user": user,
    }


@pytest.fixture
def user_graphql_info(user_graphql_context):
    return Mock(context=user_graphql_context)


@pytest.fixture
async def thread_and_post(category):
    thread = await create_thread(category, "Thread", starter_name="Guest")
    post = await create_post(thread, {"test": "yes"}, poster_name="Guest")
    thread = await update_thread(thread, first_post=post, last_post=post)
    return thread, post


@pytest.fixture
def thread(thread_and_post):
    thread, _ = thread_and_post
    return thread


@pytest.fixture
def post(thread_and_post):
    _, post = thread_and_post
    return post


@pytest.fixture
async def reply(thread):
    reply = await create_post(thread, {"test": "reply"}, poster_name="Guest")
    await update_thread(thread, last_post=reply)
    return reply


@pytest.fixture
async def user_thread_and_post(category, user):
    thread = await create_thread(category, "Thread", starter_name="Guest")
    post = await create_post(thread, {"test": "yes"}, poster=user)
    thread = await update_thread(thread, first_post=post, last_post=post)
    return thread, post


@pytest.fixture
def user_thread(user_thread_and_post):
    thread, _ = user_thread_and_post
    return thread


@pytest.fixture
def user_post(user_thread_and_post):
    _, post = user_thread_and_post
    return post
