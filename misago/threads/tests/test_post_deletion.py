import pytest

from ..delete import delete_thread_post, delete_thread_posts
from ..models import Post


@pytest.mark.asyncio
async def test_thread_post_is_deleted(thread_with_reply, thread_reply):
    await delete_thread_post(thread_with_reply, thread_reply)

    with pytest.raises(Post.DoesNotExist):
        await thread_reply.fetch_from_db()


@pytest.mark.asyncio
async def test_thread_post_delete_updates_thread_last_post_data(
    thread_with_reply, thread_reply
):
    updated_thread, last_post = await delete_thread_post(
        thread_with_reply, thread_reply
    )
    assert updated_thread.last_post_id != thread_reply.id
    assert updated_thread.last_posted_at != thread_reply.posted_at
    assert updated_thread.last_post_id == last_post.id


@pytest.mark.asyncio
async def test_thread_post_delete_updates_thread_replies_count(
    thread_with_reply, thread_reply
):
    updated_thread, _ = await delete_thread_post(thread_with_reply, thread_reply)
    assert updated_thread.replies == 0


@pytest.mark.asyncio
async def test_thread_posts_are_deleted(thread_with_reply, thread_reply):
    await delete_thread_posts(thread_with_reply, [thread_reply])

    with pytest.raises(Post.DoesNotExist):
        await thread_reply.fetch_from_db()


@pytest.mark.asyncio
async def test_thread_posts_delete_updates_thread_last_post_data(
    thread_with_reply, thread_reply
):
    updated_thread, last_post = await delete_thread_posts(
        thread_with_reply, [thread_reply]
    )
    assert updated_thread.last_post_id != thread_reply.id
    assert updated_thread.last_posted_at != thread_reply.posted_at
    assert updated_thread.last_post_id == last_post.id


@pytest.mark.asyncio
async def test_thread_posts_delete_updates_thread_replies_count(
    thread_with_reply, thread_reply
):
    updated_thread, _ = await delete_thread_posts(thread_with_reply, [thread_reply])
    assert updated_thread.replies == 0
