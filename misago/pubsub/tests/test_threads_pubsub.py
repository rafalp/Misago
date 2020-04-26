import json

import pytest

from ..threads import THREADS_CHANNEL, publish_thread_update, threads_updates


@pytest.fixture
def message(thread):
    return json.dumps({"id": thread.id, "category_id": thread.category_id})


@pytest.mark.asyncio
async def test_threads_event_is_published(publish, thread, message):
    await publish_thread_update(thread)
    publish.assert_called_once_with(channel=THREADS_CHANNEL, message=message)


@pytest.mark.asyncio
async def test_threads_updates_subscriber_returns_thread_event(
    mock_subscribe, thread, message
):
    mock_subscribe(THREADS_CHANNEL, message)
    events = [event async for event in threads_updates()]
    assert events == [{"id": thread.id, "category_id": thread.category_id}]
