import pytest

from ...passwords import check_password
from ...utils import timezone


@pytest.mark.asyncio
async def test_user_name_is_updated(user):
    updated_user = await user.update(name="Lorem")
    assert updated_user.name == "Lorem"
    assert updated_user.slug == "lorem"


@pytest.mark.asyncio
async def test_user_email_is_updated(user):
    updated_user = await user.update(email="lorem@ipsum.com")
    assert updated_user.email == "lorem@ipsum.com"
    assert updated_user.email_hash != user.email_hash


@pytest.mark.asyncio
async def test_user_full_name_is_updated(user):
    updated_user = await user.update(full_name="John Doe")
    assert updated_user.full_name == "John Doe"


@pytest.mark.asyncio
async def test_user_full_name_is_removed(user):
    updated_user = await user.update(full_name="")
    assert updated_user.full_name is None


@pytest.mark.asyncio
async def test_user_password_is_changed(user):
    updated_user = await user.update(password=" secr3t! ")
    assert updated_user.password != user.password
    assert await check_password(" secr3t! ", updated_user.password)


@pytest.mark.asyncio
async def test_user_is_made_inactive(user):
    updated_user = await user.update(is_active=False)
    assert not updated_user.is_active


@pytest.mark.asyncio
async def test_inactive_user_is_made_active(inactive_user):
    assert not inactive_user.is_active

    updated_user = await inactive_user.update(is_active=True)
    assert updated_user.is_active


@pytest.mark.asyncio
async def test_user_is_made_moderator(user):
    updated_user = await user.update(is_moderator=True)
    assert updated_user.is_moderator


@pytest.mark.asyncio
async def test_user_moderator_status_is_removed(moderator):
    assert moderator.is_moderator

    updated_user = await moderator.update(is_moderator=False)
    assert not updated_user.is_moderator


@pytest.mark.asyncio
async def test_user_is_made_admin(user):
    updated_user = await user.update(is_admin=True)
    assert updated_user.is_admin


@pytest.mark.asyncio
async def test_user_admin_status_is_removed(admin):
    assert admin.is_admin

    updated_user = await admin.update(is_admin=False)
    assert not updated_user.is_admin


@pytest.mark.asyncio
async def test_user_joined_at_datetime_is_updated(user):
    updated_user = await user.update(
        joined_at=timezone.now().replace(year=2020, month=1, day=15)
    )
    assert updated_user.joined_at.year == 2020
    assert updated_user.joined_at.month == 1
    assert updated_user.joined_at.day == 15


@pytest.mark.asyncio
async def test_user_extra_is_updated(user):
    updated_user = await user.update(extra={"test": "extra"})
    assert updated_user.extra == {"test": "extra"}
