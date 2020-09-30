import pytest

from ..query import (
    resolve_auth,
    resolve_categories,
    resolve_category,
    resolve_forum_stats,
    resolve_post,
    resolve_rich_text,
    resolve_settings,
    resolve_thread,
    resolve_threads,
    resolve_user,
)


@pytest.mark.asyncio
async def test_auth_resolver_returns_authenticated_user(user_graphql_info, user):
    value = await resolve_auth(None, user_graphql_info)
    assert value == user


@pytest.mark.asyncio
async def test_auth_resolver_returns_none_if_no_user_is_authenticated(graphql_info):
    value = await resolve_auth(None, graphql_info)
    assert value is None


@pytest.mark.asyncio
async def test_categories_resolver_returns_list_of_top_categories(
    category, child_category, graphql_info
):
    value = await resolve_categories(None, graphql_info)
    assert category in value
    assert child_category not in value


@pytest.mark.asyncio
async def test_category_resolver_returns_category_by_id(category, graphql_info):
    value = await resolve_category(None, graphql_info, id=str(category.id))
    assert value == category


@pytest.mark.asyncio
async def test_category_resolver_returns_none_for_nonexistent_category_id(graphql_info):
    value = await resolve_category(None, graphql_info, id="100")
    assert value is None


@pytest.mark.asyncio
async def test_thread_resolver_returns_thread_by_id(thread, graphql_info):
    value = await resolve_thread(None, graphql_info, id=str(thread.id))
    assert value == thread


@pytest.mark.asyncio
async def test_thread_resolver_returns_none_for_nonexistent_thread_id(graphql_info):
    value = await resolve_thread(None, graphql_info, id="100")
    assert value is None


@pytest.mark.asyncio
async def test_threads_resolver_returns_threads_feed(thread, graphql_info):
    value = await resolve_threads(None, graphql_info)
    assert value.items == [thread]


@pytest.mark.asyncio
async def test_threads_resolver_returns_threads_feed_for_category(
    thread, graphql_info, category
):
    value = await resolve_threads(None, graphql_info, category=str(category.id))
    assert value.items == [thread]


@pytest.mark.asyncio
async def test_threads_resolver_returns_threads_feed_for_cursor(
    graphql_info, thread, user_thread
):
    value = await resolve_threads(
        None, graphql_info, cursor=str(user_thread.last_post_id)
    )
    assert value.items == [thread]


@pytest.mark.asyncio
async def test_threads_resolver_returns_threads_feed_for_user(
    graphql_info, user, user_thread
):
    value = await resolve_threads(None, graphql_info, user=str(user.id))
    assert value.items == [user_thread]


@pytest.mark.asyncio
async def test_post_resolver_returns_post(graphql_info, post):
    value = await resolve_post(None, graphql_info, id=post.id)
    assert value == post


@pytest.mark.asyncio
async def test_post_resolver_returns_none_if_post_doesnt_exist(
    graphql_info, thread, post
):
    value = await resolve_post(None, graphql_info, id=post.id + 1)
    assert value is None


@pytest.mark.asyncio
async def test_user_resolver_returns_user_by_id(user, graphql_info):
    value = await resolve_user(None, graphql_info, id=str(user.id))
    assert value == user


@pytest.mark.asyncio
async def test_user_resolver_returns_none_for_nonexistent_user_id(graphql_info):
    value = await resolve_user(None, graphql_info, id="100")
    assert value is None


@pytest.mark.asyncio
async def test_forum_stats_resolver_returns_forum_stats(graphql_info):
    value = await resolve_forum_stats(None, graphql_info)
    assert value["id"]
    assert "threads" in value
    assert "posts" in value
    assert "users" in value


def test_settings_resolver_returns_settings_from_context(
    graphql_info, dynamic_settings
):
    value = resolve_settings(None, graphql_info)
    assert value is dynamic_settings


def test_rich_text_resolver_returns_parsed_body(graphql_info):
    assert resolve_rich_text(None, graphql_info, markup="Hello world!")
