import pytest

from ....pubsub.threads import THREADS_CHANNEL
from ..threads import threads_source


@pytest.mark.asyncio
async def test_threads_source_yields_thread_id(mock_subscribe):
    mock_subscribe(THREADS_CHANNEL, 123)
    events = [event async for event in threads_source()]
    assert events == [123]
