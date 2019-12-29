import pytest

from ..posts import load_thread_posts_page


@pytest.mark.asyncio
async def test_thread_posts_loader_loads_thread_posts_page(
    graphql_context, thread, post
):
    posts_page = await load_thread_posts_page(graphql_context, thread, page=1)
    assert posts_page.items == [post]


@pytest.mark.asyncio
async def test_thread_posts_loader_returns_none_if_page_is_invalid(
    graphql_context, thread
):
    posts_page = await load_thread_posts_page(graphql_context, thread, page=100)
    assert posts_page is None
