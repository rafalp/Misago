import pytest

from ..thread import (
    resolve_category,
    resolve_first_post,
    resolve_last_post,
    resolve_last_poster,
    resolve_starter,
)


@pytest.mark.asyncio
async def test_category_resolver_returns_thread_category(
    graphql_info, category, thread
):
    value = await resolve_category(thread, graphql_info)
    assert value == category


@pytest.mark.asyncio
async def test_first_post_resolver_returns_threads_first_post(
    graphql_info, thread, post
):
    value = await resolve_first_post(thread, graphql_info)
    assert value == post


@pytest.mark.asyncio
async def test_last_post_resolver_returns_threads_last_post(graphql_info, thread, post):
    value = await resolve_last_post(thread, graphql_info)
    assert value == post


@pytest.mark.asyncio
async def test_starter_resolver_returns_thread_starter(graphql_info, user_thread, user):
    value = await resolve_starter(user_thread, graphql_info)
    assert value == user


@pytest.mark.asyncio
async def test_starter_resolver_returns_none_if_starter_is_empty(graphql_info, thread):
    value = await resolve_starter(thread, graphql_info)
    assert value is None


@pytest.mark.asyncio
async def test_last_poster_resolver_returns_threads_last_poster(
    graphql_info, user_thread, user
):
    value = await resolve_last_poster(user_thread, graphql_info)
    assert value == user


@pytest.mark.asyncio
async def test_last_poster_resolver_returns_none_if_last_poster_is_empty(
    graphql_info, thread
):
    value = await resolve_last_poster(thread, graphql_info)
    assert value is None
