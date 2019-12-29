import pytest

from ..get import get_thread_by_id, get_threads_by_id, get_threads_feed


@pytest.mark.asyncio
async def test_thread_can_be_get_by_id(thread):
    assert thread == await get_thread_by_id(thread.id)


@pytest.mark.asyncio
async def test_getting_thread_by_nonexistent_id_returns_none(db):
    assert await get_thread_by_id(1) is None


@pytest.mark.asyncio
async def test_threads_can_be_get_by_id(thread):
    assert [thread] == await get_threads_by_id([thread.id])


@pytest.mark.asyncio
async def test_getting_threads_by_nonexistent_id_returns_empty_list(db):
    assert await get_threads_by_id([1]) == []


@pytest.mark.asyncio
async def test_threads_feed_can_be_get(thread):
    feed = await get_threads_feed(10)
    assert feed.items == [thread]


@pytest.mark.asyncio
async def test_threads_feed_can_be_filtered_by_thread_starter(
    thread, user_thread, user
):
    feed = await get_threads_feed(10, starter_id=user.id)
    assert feed.items == [user_thread]


@pytest.mark.asyncio
async def test_threads_feed_can_be_filtered_by_category(
    thread, closed_category_thread, closed_category
):
    feed = await get_threads_feed(10, categories=[closed_category])
    assert feed.items == [closed_category_thread]


@pytest.mark.asyncio
async def test_threads_feed_can_be_paginated_by_cursor(thread, user_thread):
    feed = await get_threads_feed(10, user_thread.last_post_id)
    assert feed.items == [thread]
