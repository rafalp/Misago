import pytest

from ...passwords import check_password
from ...utils import timezone
from ..create import create_user
from ..models import User


@pytest.mark.asyncio
async def test_user_is_created_in_db(db):
    user = await User.create("test", "test@example.com")
    assert user.id
    assert user == await User.query.one(id=user.id)


@pytest.mark.asyncio
async def test_user_is_created_with_slug(db):
    user = await User.create("TeST", "test@example.com")
    assert user.slug == "test"


@pytest.mark.asyncio
async def test_user_is_created_with_default_join_datetime(db):
    user = await User.create("test", "test@example.com")
    assert user.joined_at


@pytest.mark.asyncio
async def test_user_is_created_with_specified_join_datetime(db):
    joined_at = timezone.now()
    user = await User.create("test", "test@example.com", joined_at=joined_at)
    assert user.joined_at == joined_at


@pytest.mark.asyncio
async def test_user_is_created_with_useable_password(db, user_password):
    user = await User.create("test", "test@example.com", password=user_password)
    assert user.id
    assert await check_password(user_password, user.password)


@pytest.mark.asyncio
async def test_user_is_active_by_default(db):
    user = await User.create("test", "test@example.com")
    assert user.is_active


@pytest.mark.asyncio
async def test_user_is_created_with_inactive_status(db):
    user = await User.create("test", "test@example.com", is_active=False)
    assert not user.is_active


@pytest.mark.asyncio
async def test_user_team_statuses_default_to_false(db):
    user = await User.create("test", "test@example.com")
    assert not user.is_moderator
    assert not user.is_admin


@pytest.mark.asyncio
async def test_user_is_created_with_moderator_status(db):
    user = await User.create("test", "test@example.com", is_moderator=True)
    assert user.is_moderator


@pytest.mark.asyncio
async def test_user_is_created_with_admin_status(db):
    user = await User.create("test", "test@example.com", is_admin=True)
    assert user.is_admin


@pytest.mark.asyncio
async def test_create_user_util_creates_user_in_db(db, user_password):
    user = await create_user(
        "TeST", "test@example.com", password=user_password, is_admin=True
    )
    assert user.id
    assert user.slug == "test"
    assert user.is_admin
    assert await check_password(user_password, user.password)
