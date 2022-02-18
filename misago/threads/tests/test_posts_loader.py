import pytest

from ..loaders import posts_loader


@pytest.mark.asyncio
async def test_posts_loader_loads_post(post):
    context = {}
    posts_loader.setup_context(context)

    loaded_post = await posts_loader.load(context, post.id)
    assert loaded_post == post


@pytest.mark.asyncio
async def test_posts_loader_loads_post_url(context, thread, post):
    loaded_url = await posts_loader.load_url(context, post)
    assert loaded_url == f"/t/{thread.slug}/{thread.id}/#post-{post.id}"
