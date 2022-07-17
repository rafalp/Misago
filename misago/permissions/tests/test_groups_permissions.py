import pytest

from ..groups import get_groups_permissions
from ..permissions import CorePermission


@pytest.mark.asyncio
async def test_groups_permissions_are_retrieved(admins, moderators, members):
    assert await get_groups_permissions([admins, moderators, members])


@pytest.mark.asyncio
async def test_groups_permissions_grants_admin_perm_for_admins_group(admins, members):
    permissions = await get_groups_permissions([admins, members])
    assert CorePermission.ADMIN in permissions["core"]


@pytest.mark.asyncio
async def test_groups_permissions_grants_moderator_perm_for_moderators_group(
    moderators, members
):
    permissions = await get_groups_permissions([moderators, members])
    assert CorePermission.MODERATOR in permissions["core"]


@pytest.mark.asyncio
async def test_members_permissions_dont_grant_admin_status(members):
    permissions = await get_groups_permissions([members])
    assert CorePermission.ADMIN not in permissions["core"]


@pytest.mark.asyncio
async def test_members_permissions_dont_grant_moderator_status(members):
    permissions = await get_groups_permissions([members])
    assert CorePermission.MODERATOR not in permissions["core"]
