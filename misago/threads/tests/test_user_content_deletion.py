import pytest

from ..delete import delete_user_posts, delete_user_threads
from ..models import Post, Thread


@pytest.mark.asyncio
async def test_user_threads_are_deleted_with_posts(category, user):
    thread = await Thread.create(category, "Thread", starter=user)
    await Post.create(thread, poster=user)
    await Post.create(thread, poster_name="Guest")

    await delete_user_threads(user)

    assert await Thread.query.count() == 0
    assert await Post.query.count() == 0


@pytest.mark.asyncio
async def test_other_users_threads_are_skipped_by_user_threads_deletion(category, user):
    thread = await Thread.create(category, "Thread", starter_name="Bob")
    await Post.create(thread, poster=user)
    await Post.create(thread, poster_name="Guest")

    await delete_user_threads(user)

    assert await Thread.query.count() == 1
    assert await Post.query.count() == 2


@pytest.mark.asyncio
async def test_user_posts_are_deleted(category, user):
    thread = await Thread.create(category, "Thread", starter_name="Bob")
    await Post.create(thread, poster_name="Guest")
    user_post = await Post.create(thread, poster=user)

    await delete_user_posts(user)

    assert await Thread.query.count() == 1
    assert await Post.query.count() == 1

    with pytest.raises(Post.DoesNotExist):
        await user_post.fetch_from_db()
