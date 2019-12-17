import pytest

from ..create import create_thread
from ..get import get_thread_by_id, get_threads_by_id


@pytest.fixture
async def thread(category):
    return await create_thread("Test thread", category, starter_name="User")


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
