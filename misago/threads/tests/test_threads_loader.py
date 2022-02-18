import pytest

from ..loaders import threads_loader


@pytest.mark.asyncio
async def test_threads_loader_loads_thread(context, thread):
    loaded_thread = await threads_loader.load(context, thread.id)
    assert loaded_thread == thread
