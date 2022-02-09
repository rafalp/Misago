import pytest

from ..get import get_posts_by_id, get_thread_posts_paginator


@pytest.mark.asyncio
async def test_posts_can_be_get_by_id(post):
    assert [post] == await get_posts_by_id([post.id])


@pytest.mark.asyncio
async def test_getting_posts_by_nonexistant_id_returns_empty_list(db):
    assert await get_posts_by_id([1]) == []


@pytest.mark.asyncio
async def test_thread_posts_paginator_can_be_get(thread, post):
    paginator = await get_thread_posts_paginator(thread, 10, 0)
    assert paginator.total_pages == 1
    assert paginator.total_count == 1


@pytest.mark.asyncio
async def test_thread_posts_page_can_be_get(thread, post):
    paginator = await get_thread_posts_paginator(thread, 10, 0)
    page = await paginator.get_page(1)
    assert post.thread_id == thread.id
    assert page.results == [post]


@pytest.mark.asyncio
async def test_empty_page_is_returned_for_thread_posts_page_if_page_number_is_invalid(
    thread, post
):
    paginator = await get_thread_posts_paginator(thread, 10, 0)
    page = await paginator.get_page(100)
    assert page.total_pages == 1
    assert page.total_count == 1
    assert page.results == []
    assert page.page_info.number == 100
    assert page.page_info.has_next is False
    assert page.page_info.has_previous is True
