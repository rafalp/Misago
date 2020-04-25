import pytest

from ..get import get_updated_threads_count


@pytest.mark.asyncio
async def test_empty_threads_table_returns_no_updated_threads_count(db):
    updated_threads = await get_updated_threads_count(10, 0)
    assert updated_threads == 0


@pytest.mark.asyncio
async def test_threads_with_last_post_id_greater_than_cursor_count_as_updated(thread):
    updated_threads = await get_updated_threads_count(10, thread.last_post_id - 1)
    assert updated_threads == 1


@pytest.mark.asyncio
async def test_threads_with_last_post_id_equal_to_cursor_dont_count_as_updated(thread):
    updated_threads = await get_updated_threads_count(10, thread.last_post_id)
    assert updated_threads == 0


@pytest.mark.asyncio
async def test_threads_with_last_post_id_less_than_cursor_dont_count_as_updated(thread):
    updated_threads = await get_updated_threads_count(10, thread.last_post_id + 1)
    assert updated_threads == 0
