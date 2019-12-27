import pytest

from ..threads import (
    clear_all_threads,
    clear_thread,
    clear_threads,
    load_thread,
    load_threads,
    store_thread,
    store_threads,
)


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


@pytest.mark.asyncio
async def test_thread_is_stored_in_loader_for_future_use(thread):
    context = {}
    store_thread(context, thread)
    loaded_thread = await load_thread(context, thread.id)
    assert id(loaded_thread) == id(thread)


@pytest.mark.asyncio
async def test_threads_are_stored_in_loader_for_future_use(thread):
    context = {}
    store_threads(context, [thread])
    loaded_thread = await load_thread(context, thread.id)
    assert id(loaded_thread) == id(thread)


@pytest.mark.asyncio
async def test_thread_is_cleared_from_loader(thread):
    context = {}
    loaded_thread = await load_thread(context, thread.id)
    clear_thread(context, thread)
    new_loaded_thread = await load_thread(context, thread.id)
    assert id(loaded_thread) != id(new_loaded_thread)


@pytest.mark.asyncio
async def test_threads_are_cleared_from_loader(thread):
    context = {}
    loaded_thread = await load_thread(context, thread.id)
    clear_threads(context, [thread])
    new_loaded_thread = await load_thread(context, thread.id)
    assert id(loaded_thread) != id(new_loaded_thread)


@pytest.mark.asyncio
async def test_all_threads_are_cleared_from_loader(thread):
    context = {}
    loaded_thread = await load_thread(context, thread.id)
    clear_all_threads(context)
    new_loaded_thread = await load_thread(context, thread.id)
    assert id(loaded_thread) != id(new_loaded_thread)
