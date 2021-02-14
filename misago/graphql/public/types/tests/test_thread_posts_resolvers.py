import pytest

from .....threads.get import get_thread_posts_paginator
from ..threadposts import resolve_page, resolve_pagination


@pytest.fixture
async def paginator(thread, post):
    return await get_thread_posts_paginator(thread, 10)


@pytest.mark.asyncio
async def test_page_resolver_returns_first_thread_posts_page_by_default(
    graphql_info, paginator, post
):
    value = await resolve_page(paginator, graphql_info)
    assert value.number == 1
    assert value.items == [post]


@pytest.mark.asyncio
async def test_page_resolver_returns_specified_thread_posts_page(
    graphql_info, paginator, post
):
    value = await resolve_page(paginator, graphql_info, page=1)
    assert value.number == 1
    assert value.items == [post]


@pytest.mark.asyncio
async def test_page_resolver_returns_none_for_too_large_page_number(
    graphql_info, paginator
):
    value = await resolve_page(paginator, graphql_info, page=100)
    assert value is None


def test_thread_posts_pagination_resolver_returns_thread_posts_paginator(
    graphql_info, paginator
):
    value = resolve_pagination(paginator, graphql_info)
    assert value == paginator
