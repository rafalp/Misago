import pytest

from ..auth import authenticate


@pytest.mark.asyncio
async def test_user_is_authenticated_by_username(user, user_password):
    authenticated_user = await authenticate({}, user.name, user_password)
    assert authenticated_user == user


@pytest.mark.asyncio
async def test_user_is_authenticated_by_email(user, user_password):
    authenticated_user = await authenticate({}, user.email, user_password)
    assert authenticated_user == user


@pytest.mark.asyncio
async def test_nonexisting_user_is_not_authenticated(db, user_password):
    authenticated_user = await authenticate({}, "none@example.com", user_password)
    assert authenticated_user is None


@pytest.mark.asyncio
async def test_deactivated_user_is_not_authenticated(deactivated_user, user_password):
    authenticated_user = await authenticate({}, deactivated_user.email, user_password)
    assert authenticated_user is None


@pytest.mark.asyncio
async def test_user_without_password_is_not_authenticated(
    no_password_user, user_password
):
    authenticated_user = await authenticate({}, no_password_user.email, user_password)
    assert authenticated_user is None


@pytest.mark.asyncio
async def test_user_is_not_authenticated_if_password_is_invalid(user):
    authenticated_user = await authenticate({}, user.email, "invalid")
    assert authenticated_user is None
