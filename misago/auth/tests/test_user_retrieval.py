import pytest

from ..user import get_user


@pytest.mark.asyncio
async def test_auth_retrieves_user_by_id(context, user):
    auth_user = await get_user(context, user.id)
    assert auth_user == user


@pytest.mark.asyncio
async def test_auth_doesnt_return_inactive_user(context, inactive_user):
    auth_user = await get_user(context, inactive_user.id)
    assert auth_user is None


@pytest.mark.asyncio
async def test_auth_returns_none_for_nonexisting_user(context):
    auth_user = await get_user(context, 1)
    assert auth_user is None
