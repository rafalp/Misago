import pytest

from ..loaders import users_groups_loader, users_loader


@pytest.mark.asyncio
async def test_users_loader_loads_user(context, user):
    loaded_user = await users_loader.load(context, user.id)
    assert loaded_user == user


@pytest.mark.asyncio
async def test_users_groups_loader_loads_users_group(context, admins):
    loaded_group = await users_groups_loader.load(context, admins.id)
    assert loaded_group == admins
