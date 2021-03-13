import pytest

from ..auth import authenticate_user


@pytest.mark.asyncio
async def test_user_is_authenticated_by_username(user, user_password):
    authenticated_user = await authenticate_user({}, user.name, user_password)
    assert authenticated_user == user


@pytest.mark.asyncio
async def test_user_is_authenticated_by_email(user, user_password):
    authenticated_user = await authenticate_user({}, user.email, user_password)
    assert authenticated_user == user


@pytest.mark.asyncio
async def test_nonexisting_user_is_not_authenticated(db, user_password):
    authenticated_user = await authenticate_user({}, "none@example.com", user_password)
    assert authenticated_user is None


@pytest.mark.asyncio
async def test_inactive_user_is_not_authenticated(inactive_user, user_password):
    authenticated_user = await authenticate_user({}, inactive_user.email, user_password)
    assert authenticated_user is None


@pytest.mark.asyncio
async def test_user_without_password_is_not_authenticated(
    no_password_user, user_password
):
    authenticated_user = await authenticate_user(
        {}, no_password_user.email, user_password
    )
    assert authenticated_user is None


@pytest.mark.asyncio
async def test_user_is_not_authenticated_if_password_is_invalid(user):
    authenticated_user = await authenticate_user({}, user.email, "invalid")
    assert authenticated_user is None
