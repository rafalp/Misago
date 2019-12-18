import pytest

from ..post import resolve_category, resolve_poster, resolve_thread


@pytest.mark.asyncio
async def test_category_resolver_returns_post_category(graphql_info, category, post):
    value = await resolve_category(post, graphql_info)
    assert value == category


@pytest.mark.asyncio
async def test_post_resolver_returns_post_poster(graphql_info, user_post, user):
    value = await resolve_poster(user_post, graphql_info)
    assert value == user


@pytest.mark.asyncio
async def test_post_resolver_returns_none_if_poster_is_empty(graphql_info, post):
    value = await resolve_poster(post, graphql_info)
    assert value is None


@pytest.mark.asyncio
async def test_post_resolver_returns_post_thread(graphql_info, post, thread):
    value = await resolve_thread(post, graphql_info)
    assert value == thread
