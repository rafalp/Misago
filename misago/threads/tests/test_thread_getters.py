import pytest

from ..get import get_threads_by_id


@pytest.fixture
def threads(thread, user_thread, closed_thread):
    return sorted(
        [thread, user_thread, closed_thread], key=lambda x: x.last_post_id, reverse=True
    )


@pytest.mark.asyncio
async def test_threads_can_be_get_by_id(thread):
    assert [thread] == await get_threads_by_id([thread.id])


@pytest.mark.asyncio
async def test_getting_threads_by_nonexistant_id_returns_empty_list(db):
    assert await get_threads_by_id([1]) == []
