import pytest

from ..permissions import CategoryPermission, CorePermission
from ..users import get_user_permissions


@pytest.mark.asyncio
async def test_user_permissions_are_returned(context, user, members):
    assert await get_user_permissions(context, user)


@pytest.mark.asyncio
async def test_user_without_admin_permission(context, user, members):
    perms = await get_user_permissions(context, user)
    assert CorePermission.ADMIN not in perms["core"]


@pytest.mark.asyncio
async def test_user_with_admin_permission_from_group(context, user, members, admins):
    user = await user.update_groups(members, [admins])
    perms = await get_user_permissions(context, user)
    assert CorePermission.ADMIN in perms["core"]


@pytest.mark.asyncio
async def test_user_with_admin_permission_from_user(context, user, members):
    user = await user.update(is_admin=True)
    perms = await get_user_permissions(context, user)
    assert CorePermission.ADMIN in perms["core"]


@pytest.mark.asyncio
async def test_user_without_moderator_permission(context, user, members):
    perms = await get_user_permissions(context, user)
    assert CorePermission.MODERATOR not in perms["core"]


@pytest.mark.asyncio
async def test_user_with_moderator_permission_from_group(
    context, user, members, moderators
):
    user = await user.update_groups(members, [moderators])
    perms = await get_user_permissions(context, user)
    assert CorePermission.MODERATOR in perms["core"]


@pytest.mark.asyncio
async def test_user_with_moderator_permission_from_user(context, user, members):
    user = await user.update(is_moderator=True)
    perms = await get_user_permissions(context, user)
    assert CorePermission.MODERATOR in perms["core"]
