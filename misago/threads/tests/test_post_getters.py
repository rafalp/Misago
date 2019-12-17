import pytest

from ..create import create_post, create_thread
from ..get import get_post_by_id, get_posts_by_id


@pytest.fixture
async def post(category):
    thread = await create_thread("Test thread", category, starter_name="User")
    return await create_post({}, thread, category, poster_name="User")


@pytest.mark.asyncio
async def test_post_can_be_get_by_id(post):
    assert post == await get_post_by_id(post.id)


@pytest.mark.asyncio
async def test_getting_post_by_nonexistent_id_returns_none(db):
    assert await get_post_by_id(1) is None


@pytest.mark.asyncio
async def test_posts_can_be_get_by_id(post):
    assert [post] == await get_posts_by_id([post.id])


@pytest.mark.asyncio
async def test_getting_posts_by_nonexistent_id_returns_empty_list(db):
    assert await get_posts_by_id([1]) == []
