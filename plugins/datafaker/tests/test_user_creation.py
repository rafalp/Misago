import pytest

from ..users import create_fake_user


@pytest.mark.asyncio
async def test_fake_user_is_created(db, faker):
    assert await create_fake_user(faker)


@pytest.mark.asyncio
async def test_multiple_fake_users_are_created(db, faker):
    for _ in range(5):
        assert await create_fake_user(faker)
