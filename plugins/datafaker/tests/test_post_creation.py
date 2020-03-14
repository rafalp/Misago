import pytest

from ..threads import create_fake_post


@pytest.mark.asyncio
async def test_fake_post_is_created(thread, user):
    assert await create_fake_post(thread, poster=user)


@pytest.mark.asyncio
async def test_multiple_fake_posts_are_created(thread, user):
    for _ in range(5):
        assert await create_fake_post(thread, poster=user)
