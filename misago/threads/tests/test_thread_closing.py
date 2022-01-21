import pytest

from ..close import close_threads, open_threads


@pytest.mark.asyncio
async def test_open_threads_can_be_closed(thread):
    threads = await close_threads([thread])
    assert threads[0].is_closed
    thread_from_db = await thread.refresh_from_db()
    assert thread_from_db.is_closed


@pytest.mark.asyncio
async def test_already_closed_threads_are_skipped(closed_thread):
    threads = await close_threads([closed_thread])
    assert threads == []


@pytest.mark.asyncio
async def test_closed_threads_can_be_opened(closed_thread):
    threads = await open_threads([closed_thread])
    assert not threads[0].is_closed
    thread_from_db = await closed_thread.refresh_from_db()
    assert not thread_from_db.is_closed


@pytest.mark.asyncio
async def test_already_open_threads_are_skipped(thread):
    threads = await open_threads([thread])
    assert threads == []
