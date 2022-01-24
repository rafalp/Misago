import pytest

from ...utils import timezone
from ..models import Post, Thread


@pytest.fixture
async def thread(category):
    return await Thread.create(category, "Test thread", starter_name="User")


@pytest.mark.asyncio
async def test_post_is_created_in_db(thread):
    post = await Post.create(thread, poster_name="User")
    assert post.id
    assert post == await post.fetch_from_db()


@pytest.mark.asyncio
async def test_post_is_created_with_category_and_thread(thread):
    post = await Post.create(thread, poster_name="User")
    assert post.category_id == thread.category_id
    assert post.thread_id == thread.id


@pytest.mark.asyncio
async def test_post_is_created_with_posted_datetime(thread):
    post = await Post.create(thread, poster_name="User")
    assert post.posted_at


@pytest.mark.asyncio
async def test_post_is_created_with_explicit_posted_datetime(thread):
    posted_at = timezone.now()
    post = await Post.create(thread, poster_name="User", posted_at=posted_at)
    assert post.posted_at == posted_at


@pytest.mark.asyncio
async def test_post_is_created_with_removed_poster(thread):
    post = await Post.create(thread, poster_name="User")
    assert post.poster_id is None
    assert post.poster_name == "User"


@pytest.mark.asyncio
async def test_post_is_created_with_poster(thread, user):
    post = await Post.create(thread, poster=user)
    assert post.poster_id == user.id
    assert post.poster_name == user.name
