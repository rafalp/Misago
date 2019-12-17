import pytest

from ..threads import load_thread, load_threads


@pytest.mark.asyncio
async def test_thread_loader_returns_thread(thread):
    loaded_thread = await load_thread({}, thread.id)
    assert loaded_thread == thread


@pytest.mark.asyncio
async def test_thread_loader_returns_none_for_nonexistent_thread_id(db):
    loaded_thread = await load_thread({}, 1)
    assert loaded_thread is None


@pytest.mark.asyncio
async def test_threads_loader_returns_multiple_threads(thread, user_thread):
    loaded_threads = await load_threads({}, [thread.id, user_thread.id])
    assert loaded_threads == [thread, user_thread]


@pytest.mark.asyncio
async def test_threads_loader_returns_none_for_nonexistent_thread_id(thread):
    loaded_threads = await load_threads({}, [thread.id, thread.id + 1])
    assert loaded_threads == [thread, None]
