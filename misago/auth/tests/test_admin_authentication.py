import pytest

from ..auth import authenticate_admin


@pytest.mark.asyncio
async def test_admin_is_authenticated_by_username(admin, user_password):
    authenticated_admin = await authenticate_admin({}, admin.name, user_password)
    assert authenticated_admin == admin


@pytest.mark.asyncio
async def test_admin_is_authenticated_by_email(admin, user_password):
    authenticated_admin = await authenticate_admin({}, admin.email, user_password)
    assert authenticated_admin == admin


@pytest.mark.asyncio
async def test_nonexisting_admin_is_not_authenticated(db, user_password):
    authenticated_admin = await authenticate_admin(
        {}, "none@example.com", user_password
    )
    assert authenticated_admin is None


@pytest.mark.asyncio
async def test_deactivated_admin_is_not_authenticated(deactivated_admin, user_password):
    authenticated_admin = await authenticate_admin(
        {}, deactivated_admin.email, user_password
    )
    assert authenticated_admin is None


@pytest.mark.asyncio
async def test_admin_without_password_is_not_authenticated(
    no_password_admin, user_password
):
    authenticated_admin = await authenticate_admin(
        {}, no_password_admin.email, user_password
    )
    assert authenticated_admin is None


@pytest.mark.asyncio
async def test_admin_is_not_authenticated_if_password_is_invalid(admin, user_password):
    authenticated_admin = await authenticate_admin({}, admin.email, "invalid")
    assert authenticated_admin is None
