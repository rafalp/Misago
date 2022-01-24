import pytest

from ..models import Post, Thread


@pytest.mark.asyncio
async def test_thread_is_deleted(thread):
    await thread.delete()

    with pytest.raises(Thread.DoesNotExist):
        await thread.fetch_from_db()


@pytest.mark.asyncio
async def test_thread_post_is_deleted_together_with_thread(thread, post):
    await thread.delete()

    with pytest.raises(Post.DoesNotExist):
        await post.fetch_from_db()
