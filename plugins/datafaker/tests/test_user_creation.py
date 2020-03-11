import pytest

from ..users import create_fake_user


@pytest.mark.asyncio
async def test_fake_user_is_created(db, faker):
    assert await create_fake_user(faker)
