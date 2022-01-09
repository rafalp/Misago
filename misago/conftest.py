from tempfile import TemporaryDirectory
from typing import Optional
from unittest.mock import AsyncMock, Mock, patch

import httpx
import pytest

from . import tables
from .asgi import app
from .categories.models import Category
from .conf.cache import SETTINGS_CACHE
from .conf.dynamicsettings import get_dynamic_settings
from .database import database
from .database.testdatabase import create_test_database, teardown_test_database
from .threads.models import Post, Thread
from .users.models import User


def pytest_configure():
    create_test_database()


def pytest_unconfigure():
    teardown_test_database()


@pytest.fixture
async def db():
    await database.connect()
    yield
    await database.disconnect()


@pytest.fixture
def publish(mocker):
    return mocker.patch("misago.pubsub.broadcast.publish")


@pytest.fixture
def mock_subscribe(mocker):
    def patch_subscribe(expected_channel: str, message: any):
        async def _mock_subscribe():
            yield Mock(message=str(message))

        class MockSubscribe:
            def __init__(self, *, channel):
                assert expected_channel == channel

            async def __aenter__(self):
                return _mock_subscribe()

            async def __aexit__(self, *args, **kwargs):
                pass

        return mocker.patch("misago.pubsub.broadcast.subscribe", MockSubscribe)

    return patch_subscribe


@pytest.fixture
def mock_media_dir():
    with TemporaryDirectory() as tmp_media_dir:
        with patch("misago.conf.settings._media_root", tmp_media_dir):
            yield tmp_media_dir


@pytest.fixture
def cache_versions():
    return {SETTINGS_CACHE: "settings-cache"}


@pytest.fixture
async def cache_version(db):
    query = tables.cache_versions.insert(None).values(
        cache="test_cache", version="version"
    )
    await database.execute(query)
    return {"cache": "test_cache", "version": "version"}


@pytest.fixture
async def other_cache_version(db):
    query = tables.cache_versions.insert(None).values(
        cache="test_other_cache", version="version"
    )
    await database.execute(query)
    return {"cache": "test_other_cache", "version": "version"}


@pytest.fixture
async def dynamic_settings(db, cache_versions):
    return await get_dynamic_settings(cache_versions)


@pytest.fixture
async def categories(db):
    top_category = await Category.create(name="Category", left=3, right=6)
    child_category = await Category.create(
        name="Child Category", parent=top_category, left=4, right=5, depth=1
    )
    sibling_category = await Category.create(name="Sibling Category", left=7, right=8)
    closed_category = await Category.create(
        name="Closed Category", left=9, right=10, is_closed=True
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
    return await User.create("User", "user@example.com", password=user_password)


@pytest.fixture
async def other_user(db, user_password):
    return await User.create(
        "OtherUser", "other-user@example.com", password=user_password
    )


@pytest.fixture
async def inactive_user(db, user_password):
    return await User.create(
        "User", "inactive@example.com", password=user_password, is_active=False
    )


@pytest.fixture
async def no_password_user(db):
    return await User.create("NopassUser", "nopass-user@example.com")


@pytest.fixture
async def moderator(db, user_password):
    return await User.create(
        "Moderator", "moderator@example.com", password=user_password, is_moderator=True
    )


@pytest.fixture
async def admin(db, user_password):
    return await User.create(
        "Admin", "admin@example.com", password=user_password, is_admin=True
    )


@pytest.fixture
def request_mock():
    return Mock(headers={}, base_url="http://test.com/", user=None)


@pytest.fixture
def graphql_context(request_mock, cache_versions, dynamic_settings):
    return {
        "request": request_mock,
        "cache_versions": cache_versions,
        "settings": dynamic_settings,
        "user": None,
    }


@pytest.fixture
def graphql_info(graphql_context):
    return Mock(context=graphql_context)


@pytest.fixture
def user_graphql_context(request_mock, cache_versions, dynamic_settings, user):
    return {
        "request": request_mock,
        "cache_versions": cache_versions,
        "settings": dynamic_settings,
        "user": user,
    }


@pytest.fixture
def user_graphql_info(user_graphql_context):
    return Mock(context=user_graphql_context)


@pytest.fixture
def moderator_graphql_context(
    request_mock, cache_versions, dynamic_settings, moderator
):
    return {
        "request": request_mock,
        "cache_versions": cache_versions,
        "settings": dynamic_settings,
        "user": moderator,
    }


@pytest.fixture
def moderator_graphql_info(moderator_graphql_context):
    return Mock(context=moderator_graphql_context)


@pytest.fixture
def admin_graphql_context(request_mock, cache_versions, dynamic_settings, admin):
    return {
        "request": request_mock,
        "cache_versions": cache_versions,
        "settings": dynamic_settings,
        "checked_admin_auth": True,
        "user": admin,
    }


@pytest.fixture
def admin_graphql_info(admin_graphql_context):
    return Mock(context=admin_graphql_context)


@pytest.fixture
async def thread_and_post(category):
    thread = await Thread.create(category, "Thread", starter_name="Guest")
    post = await Post.create(thread, poster_name="Guest")
    thread = await thread.update(first_post=post, last_post=post)
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
    reply = await Post.create(thread, poster_name="Guest")
    await thread.update(replies=1, last_post=reply)
    return reply


@pytest.fixture
async def thread_and_reply(thread):
    reply = await Post.create(thread, poster_name="Guest")
    thread = await thread.update(replies=1, last_post=reply)
    return thread, reply


@pytest.fixture
async def thread_with_reply(thread_and_reply):
    thread, _ = thread_and_reply
    return thread


@pytest.fixture
async def thread_reply(thread_and_reply):
    _, reply = thread_and_reply
    return reply


@pytest.fixture
async def user_thread_and_post(category, user):
    thread = await Thread.create(category, "Thread", starter_name="Guest")
    post = await Post.create(thread, poster=user)
    thread = await thread.update(first_post=post, last_post=post)
    return thread, post


@pytest.fixture
def user_thread(user_thread_and_post):
    thread, _ = user_thread_and_post
    return thread


@pytest.fixture
def user_post(user_thread_and_post):
    _, post = user_thread_and_post
    return post


@pytest.fixture
async def other_user_thread_and_post(category, other_user):
    thread = await Thread.create(category, "Thread", starter_name="Guest")
    post = await Post.create(thread, poster=other_user)
    thread = await thread.update(first_post=post, last_post=post)
    return thread, post


@pytest.fixture
def other_user_thread(other_user_thread_and_post):
    thread, _ = other_user_thread_and_post
    return thread


@pytest.fixture
def other_user_post(other_user_thread_and_post):
    _, post = other_user_thread_and_post
    return post


@pytest.fixture
async def closed_thread_and_post(category):
    thread = await Thread.create(
        category, "Thread", starter_name="Guest", is_closed=True
    )
    post = await Post.create(thread, poster_name="Guest")
    thread = await thread.update(first_post=post, last_post=post)
    return thread, post


@pytest.fixture
def closed_thread(closed_thread_and_post):
    thread, _ = closed_thread_and_post
    return thread


@pytest.fixture
def closed_thread_post(closed_thread_and_post):
    _, post = closed_thread_and_post
    return post


@pytest.fixture
async def closed_category_thread_and_post(closed_category):
    thread = await Thread.create(
        closed_category,
        "Closed Category Thread",
        starter_name="Guest",
    )
    post = await Post.create(thread, poster_name="Guest")
    thread = await thread.update(first_post=post, last_post=post)
    return thread, post


@pytest.fixture
def closed_category_thread(closed_category_thread_and_post):
    thread, _ = closed_category_thread_and_post
    return thread


@pytest.fixture
def closed_category_post(closed_category_thread_and_post):
    _, post = closed_category_thread_and_post
    return post


@pytest.fixture
async def closed_user_thread_and_post(category, user):
    thread = await Thread.create(
        category, "Thread", starter_name="Guest", is_closed=True
    )
    post = await Post.create(thread, poster=user)
    thread = await thread.update(first_post=post, last_post=post)
    return thread, post


@pytest.fixture
def closed_user_thread(closed_user_thread_and_post):
    thread, _ = closed_user_thread_and_post
    return thread


@pytest.fixture
def closed_user_thread_post(closed_user_thread_and_post):
    _, post = closed_user_thread_and_post
    return post


@pytest.fixture
async def closed_category_user_thread_and_post(closed_category, user):
    thread = await Thread.create(closed_category, "Thread", starter_name="Guest")
    post = await Post.create(thread, poster=user)
    thread = await thread.update(first_post=post, last_post=post)
    return thread, post


@pytest.fixture
def closed_category_user_thread(closed_category_user_thread_and_post):
    thread, _ = closed_category_user_thread_and_post
    return thread


@pytest.fixture
def closed_category_user_post(closed_category_user_thread_and_post):
    _, post = closed_category_user_thread_and_post
    return post


@pytest.fixture
def http_client():
    def create_http_client():
        return httpx.AsyncClient(app=app, base_url="http://example.com")

    return create_http_client


@pytest.fixture
def query_admin_api(http_client, admin, monkeypatch):
    async def query_admin_schema(
        query, variables=None, *, include_auth: bool = True, expect_error: bool = False
    ):
        if include_auth:
            monkeypatch.setattr(
                "misago.auth.auth.get_user_from_context",
                AsyncMock(return_value=admin),
            )

        async with http_client() as client:
            r = await client.post(
                "/admin/graphql/", json={"query": query, "variables": variables}
            )
            result = r.json()
            if not expect_error:
                assert not "errors" in result, "GraphQL query could not be completed"
            else:
                assert "errors" in result, "GraphQL expected to error"

            return result

    return query_admin_schema


@pytest.fixture
def query_public_api(http_client, monkeypatch):
    async def query_public_schema(
        query, variables=None, *, auth: Optional[User] = None
    ):
        if auth:
            monkeypatch.setattr(
                "misago.auth.auth.get_user_from_context",
                AsyncMock(return_value=auth),
            )

        async with http_client() as client:
            r = await client.post(
                "/graphql/", json={"query": query, "variables": variables}
            )
            return r.json()

    return query_public_schema
