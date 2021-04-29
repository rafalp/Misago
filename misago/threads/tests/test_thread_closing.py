import pytest

from ..close import close_thread, close_threads


@pytest.mark.asyncio
async def test_open_thread_can_be_closed(thread):
    closed_thread = await close_thread(thread, True)
    assert closed_thread.is_closed
    thread_from_db = await thread.refresh_from_db()
    assert thread_from_db.is_closed


@pytest.mark.asyncio
async def test_closed_thread_can_be_opened(closed_thread):
    thread = await close_thread(closed_thread, False)
    assert not thread.is_closed
    thread_from_db = await closed_thread.refresh_from_db()
    assert not thread_from_db.is_closed


@pytest.mark.asyncio
async def test_open_threads_can_be_closed(thread):
    threads = await close_threads([thread], True)
    assert threads[0].is_closed
    thread_from_db = await thread.refresh_from_db()
    assert thread_from_db.is_closed


@pytest.mark.asyncio
async def test_closed_threads_can_be_opened(closed_thread):
    threads = await close_threads([closed_thread], False)
    assert not threads[0].is_closed
    thread_from_db = await closed_thread.refresh_from_db()
    assert not thread_from_db.is_closed
