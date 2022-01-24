import pytest

from ...threads.models import Post, Thread
from ..delete import delete_user_content


@pytest.mark.asyncio
async def test_delete_user_content_util_deletes_user_threads_and_posts(
    user, user_thread, user_post
):
    await delete_user_content(user)

    with pytest.raises(Thread.DoesNotExist):
        await user_thread.fetch_from_db()

    with pytest.raises(Post.DoesNotExist):
        await user_post.fetch_from_db()


@pytest.mark.asyncio
async def test_delete_user_content_util_omits_other_users_content(
    user, other_user_thread, other_user_post
):
    await delete_user_content(user)

    assert await other_user_thread.fetch_from_db()
    assert await other_user_post.fetch_from_db()
