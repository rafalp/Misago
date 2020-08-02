import pytest

from ..posts import load_thread_posts_page, load_thread_posts_paginator


@pytest.mark.asyncio
async def test_thread_posts_paginator_loader_returns_posts_paginator(
    graphql_context, thread
):
    paginator = await load_thread_posts_paginator(graphql_context, thread)
    assert paginator.get_count() == 1
    assert paginator.get_pages() == 1


@pytest.mark.asyncio
async def test_thread_posts_loader_loads_thread_posts_page(
    graphql_context, thread, post
):
    paginator = await load_thread_posts_paginator(graphql_context, thread)
    posts_page = await load_thread_posts_page(graphql_context, paginator, page=1)
    assert posts_page.items == [post]


@pytest.mark.asyncio
async def test_thread_posts_loader_returns_none_if_page_is_invalid(
    graphql_context, thread
):
    paginator = await load_thread_posts_paginator(graphql_context, thread)
    posts_page = await load_thread_posts_page(graphql_context, paginator, page=100)
    assert posts_page is None