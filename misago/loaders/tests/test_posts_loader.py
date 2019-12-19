import pytest

from ..posts import load_post, load_posts, store_post


@pytest.mark.asyncio
async def test_post_loader_returns_post(post):
    loaded_post = await load_post({}, post.id)
    assert loaded_post == post


@pytest.mark.asyncio
async def test_post_loader_returns_none_for_nonexistent_post_id(db):
    loaded_post = await load_post({}, 1)
    assert loaded_post is None


@pytest.mark.asyncio
async def test_posts_loader_returns_multiple_posts(post, reply):
    loaded_posts = await load_posts({}, [post.id, reply.id])
    assert loaded_posts == [post, reply]


@pytest.mark.asyncio
async def test_posts_loader_returns_none_for_nonexistent_post_id(post):
    loaded_posts = await load_posts({}, [post.id, post.id + 1])
    assert loaded_posts == [post, None]


@pytest.mark.asyncio
async def test_post_is_stored_in_loader_for_future_use(post):
    context = {}
    store_post(context, post)
    loaded_post = await load_post(context, post.id)
    assert id(loaded_post) == id(post)
