import pytest

from ..loaders import users_loader


@pytest.mark.asyncio
async def test_users_loader_loads_user(context, user):
    loaded_user = await users_loader.load(context, user.id)
    assert loaded_user == user
