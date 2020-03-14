import pytest

from ..threads import create_fake_thread


@pytest.mark.asyncio
async def test_fake_thread_is_created(category, user):
    assert await create_fake_thread(category, starter=user)


@pytest.mark.asyncio
async def test_multiple_fake_threads_are_created(category, user):
    for _ in range(5):
        assert await create_fake_thread(category, starter=user)
