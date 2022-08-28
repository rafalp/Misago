import pytest

from ..groups import get_groups_permissions
from ..permissions import CorePermission


@pytest.mark.asyncio
async def test_groups_permissions_are_retrieved(context, admins, moderators, members):
    assert await get_groups_permissions(context, [admins, moderators, members])


@pytest.mark.asyncio
async def test_groups_permissions_grants_admin_perm_for_admins_group(
    context, admins, members
):
    permissions = await get_groups_permissions(context, [admins, members])
    assert CorePermission.ADMIN in permissions["core"]


@pytest.mark.asyncio
async def test_groups_permissions_grants_moderator_perm_for_moderators_group(
    context, moderators, members
):
    permissions = await get_groups_permissions(context, [moderators, members])
    assert CorePermission.MODERATOR in permissions["core"]


@pytest.mark.asyncio
async def test_members_permissions_dont_grant_admin_status(context, members):
    permissions = await get_groups_permissions(context, [members])
    assert CorePermission.ADMIN not in permissions["core"]


@pytest.mark.asyncio
async def test_members_permissions_dont_grant_moderator_status(context, members):
    permissions = await get_groups_permissions(context, [members])
    assert CorePermission.MODERATOR not in permissions["core"]
