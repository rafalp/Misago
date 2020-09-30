import pytest

from ...utils import timezone
from ..create import create_post, create_thread
from ..get import get_post_by_id


@pytest.fixture
async def thread(category):
    return await create_thread(category, "Test thread", starter_name="User")


@pytest.mark.asyncio
async def test_post_is_created_in_db(thread):
    post = await create_post(thread, poster_name="User")
    assert post.id
    assert post == await get_post_by_id(post.id)


@pytest.mark.asyncio
async def test_post_is_created_with_category_and_thread(thread):
    post = await create_post(thread, poster_name="User")
    assert post.category_id == thread.category_id
    assert post.thread_id == thread.id


@pytest.mark.asyncio
async def test_post_is_created_with_posted_datetime(thread):
    post = await create_post(thread, poster_name="User")
    assert post.posted_at


@pytest.mark.asyncio
async def test_post_is_created_with_explicit_posted_datetime(thread):
    posted_at = timezone.now()
    post = await create_post(thread, poster_name="User", posted_at=posted_at)
    assert post.posted_at == posted_at


@pytest.mark.asyncio
async def test_post_is_created_with_removed_poster(thread):
    post = await create_post(thread, poster_name="User")
    assert post.poster_id is None
    assert post.poster_name == "User"


@pytest.mark.asyncio
async def test_post_is_created_with_poster(thread, user):
    post = await create_post(thread, poster=user)
    assert post.poster_id == user.id
    assert post.poster_name == user.name
