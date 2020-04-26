import pytest

from ..threads import THREADS_CHANNEL, publish_thread_update, threads_updates


@pytest.mark.asyncio
async def test_threads_event_is_published(publish, thread):
    await publish_thread_update(thread)
    publish.assert_called_once_with(channel=THREADS_CHANNEL, message=str(thread.id))


@pytest.mark.asyncio
async def test_threads_updates_subscriber_returns_thread_event(mock_subscribe):
    mock_subscribe(THREADS_CHANNEL, 123)
    events = [event async for event in threads_updates()]
    assert events == [123]
