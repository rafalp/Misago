import pytest

from ..get import (
    get_user_by_email,
    get_user_by_name,
    get_user_by_name_or_email,
    get_users_by_id,
    get_users_by_name,
)


@pytest.mark.asyncio
async def test_multiple_users_can_be_get_by_id(user, other_user):
    users = await get_users_by_id([user.id, other_user.id, other_user.id + 100])
    assert len(users) == 2
    assert user in users
    assert other_user in users


@pytest.mark.asyncio
async def test_user_can_be_get_by_email(user):
    assert user == await get_user_by_email(user.email)


@pytest.mark.asyncio
async def test_getting_user_by_nonexistant_email_returns_none(db):
    assert await get_user_by_name("nonexistant@email.com") is None


@pytest.mark.asyncio
async def test_user_can_be_get_by_name(user):
    assert user == await get_user_by_name(user.name)


@pytest.mark.asyncio
async def test_getting_user_by_nonexistant_name_returns_none(db):
    assert await get_user_by_name("nonexistant") is None


@pytest.mark.asyncio
async def test_multiple_users_can_be_get_by_name(user, other_user):
    users = await get_users_by_name([user.name, other_user.name, "invalid"])
    assert len(users) == 2
    assert user in users
    assert other_user in users


@pytest.mark.asyncio
async def test_name_or_email_getter_returns_user_with_matching_name(user):
    assert user == await get_user_by_name_or_email(user.name)


@pytest.mark.asyncio
async def test_name_or_email_getter_returns_user_with_matching_email(user):
    assert user == await get_user_by_name_or_email(user.email)


@pytest.mark.asyncio
async def test_name_or_email_getter_returns_none_if_no_user_is_found(db):
    assert await get_user_by_name_or_email("nonexistant") is None
