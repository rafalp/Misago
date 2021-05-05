import pytest

from ..models import Post
from ..sync import get_thread_stats, sync_thread, sync_thread_by_id


@pytest.mark.asyncio
async def test_thread_stats_can_be_retrieved(thread, reply):
    new_reply = await Post.create(thread, poster_name="Guest")
    stats = await get_thread_stats(thread.id)
    assert stats["replies"] == 2
    assert stats["last_post"] == new_reply


@pytest.mark.asyncio
async def test_thread_is_synced(thread, reply):
    new_reply = await Post.create(thread, poster_name="Guest")
    updated_thread, stats = await sync_thread(thread)
    assert updated_thread.replies == 2
    assert updated_thread.last_post_id == new_reply.id
    assert stats["replies"] == 2
    assert stats["last_post"] == new_reply


@pytest.mark.asyncio
async def test_thread_is_synced_by_id(thread, reply):
    new_reply = await Post.create(thread, poster_name="Guest")
    stats = await sync_thread_by_id(thread.id)
    assert stats["replies"] == 2
    assert stats["last_post"] == new_reply

    thread_from_db = await thread.refresh_from_db()
    assert thread_from_db.replies == 2
    assert thread_from_db.last_post_id == new_reply.id
