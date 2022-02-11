import pytest

from ..loaders import users_loader


@pytest.mark.asyncio
async def test_users_loader_loads_user(graphql_context, user):
    loaded_user = await users_loader.load(graphql_context, user.id)
    assert loaded_user == user
