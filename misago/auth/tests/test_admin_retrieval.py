import pytest

from ..user import get_admin


@pytest.mark.asyncio
async def test_auth_retrieves_admin_by_id(admin):
    auth_admin = await get_admin({}, admin.id)
    assert auth_admin == admin


@pytest.mark.asyncio
async def test_auth_doesnt_return_deactivated_admin(deactivated_admin):
    auth_admin = await get_admin({}, deactivated_admin.id)
    assert auth_admin is None


@pytest.mark.asyncio
async def test_auth_returns_none_for_nonexisting_admin(db):
    auth_admin = await get_admin({}, 1)
    assert auth_admin is None
