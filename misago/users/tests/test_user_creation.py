import pytest

from ...passwords import verify_password
from ..create import create_user
from ..get import get_user_by_id


@pytest.mark.asyncio
async def test_user_is_created_in_db(db):
    user = await create_user("test", "test@example.com")
    assert user.id
    assert user == await get_user_by_id(user.id)


@pytest.mark.asyncio
async def test_user_is_created_with_join_datetime(db, user_password):
    user = await create_user("test", "test@example.com", password=user_password)
    assert user.joined_at


@pytest.mark.asyncio
async def test_user_is_created_with_useable_password(db, user_password):
    user = await create_user("test", "test@example.com", password=user_password)
    assert user.id
    assert await verify_password(user_password, user.password)


@pytest.mark.asyncio
async def test_user_is_created_with_moderator_status(db, user_password):
    user = await create_user("test", "test@example.com", is_moderator=True)
    assert user.is_moderator


@pytest.mark.asyncio
async def test_user_is_created_with_admin_status(db, user_password):
    user = await create_user("test", "test@example.com", is_admin=True)
    assert user.is_admin
