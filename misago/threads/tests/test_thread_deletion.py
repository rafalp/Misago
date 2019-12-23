import pytest

from ..delete import delete_thread, delete_threads
from ..get import get_post_by_id, get_thread_by_id


@pytest.mark.asyncio
async def test_thread_is_deleted(thread):
    await delete_thread(thread)
    assert await get_thread_by_id(thread.id) is None


@pytest.mark.asyncio
async def test_thread_post_is_deleted_together_with_thread(thread, post):
    await delete_thread(thread)
    assert await get_post_by_id(post.id) is None


@pytest.mark.asyncio
async def test_threads_are_deleted(thread):
    await delete_threads([thread])
    assert await get_thread_by_id(thread.id) is None


@pytest.mark.asyncio
async def test_threads_posts_are_deleted_together_with_threads(thread, post):
    await delete_threads([thread])
    assert await get_post_by_id(post.id) is None
