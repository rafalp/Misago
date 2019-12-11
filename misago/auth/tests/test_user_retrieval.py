import pytest

from ..user import get_user


@pytest.mark.asyncio
async def test_auth_retrieves_user_by_id(user):
    auth_user = await get_user({}, user.id)
    assert auth_user == user


@pytest.mark.asyncio
async def test_auth_doesnt_return_deactivated_user(deactivated_user):
    auth_user = await get_user({}, deactivated_user.id)
    assert auth_user is None


@pytest.mark.asyncio
async def test_auth_returns_none_for_nonexisting_user(db):
    auth_user = await get_user({}, 1)
    assert auth_user is None
