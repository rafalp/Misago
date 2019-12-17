from datetime import datetime

import pytest

from ..create import create_post, create_thread
from ..get import get_post_by_id


@pytest.fixture
async def thread(category):
    return await create_thread(category, "Test thread", starter_name="User")


@pytest.mark.asyncio
async def test_post_is_created_in_db(category, thread):
    post = await create_post(category, thread, {}, poster_name="User")
    assert post.id
    assert post == await get_post_by_id(post.id)


@pytest.mark.asyncio
async def test_post_is_created_with_category_and_thread(category, thread):
    post = await create_post(category, thread, {}, poster_name="User")
    assert post.category_id == category.id
    assert post.thread_id == thread.id


@pytest.mark.asyncio
async def test_post_is_created_with_posted_datetime(category, thread):
    post = await create_post(category, thread, {}, poster_name="User")
    assert post.posted_at


@pytest.mark.asyncio
async def test_post_is_created_with_explicit_posted_datetime(category, thread):
    posted_at = datetime.utcnow()
    post = await create_post(
        category, thread, {}, poster_name="User", posted_at=posted_at
    )
    assert post.posted_at == posted_at


@pytest.mark.asyncio
async def test_post_is_created_with_removed_poster(category, thread):
    post = await create_post(category, thread, {}, poster_name="User")
    assert post.poster_id is None
    assert post.poster_name == "User"


@pytest.mark.asyncio
async def test_post_is_created_with_poster(category, thread, user):
    post = await create_post(category, thread, {}, poster=user)
    assert post.poster_id == user.id
    assert post.poster_name == user.name
