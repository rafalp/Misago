import pytest

from ..delete import delete_thread
from ..get import get_post_by_id, get_thread_by_id


@pytest.mark.asyncio
async def test_thread_is_deleted(thread):
    await delete_thread(thread)
    assert await get_thread_by_id(thread.id) is None


@pytest.mark.asyncio
async def test_thread_post_is_deleted_together_with_thread(thread, post):
    await delete_thread(thread)
    assert await get_post_by_id(post.id) is None
