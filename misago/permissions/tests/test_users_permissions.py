import pytest

from ..permissions import CategoryPermission, CorePermission
from ..users import get_user_permissions
from ..queries import categories_permissions_query, permissions_query


@pytest.mark.asyncio
async def test_user_permissions_are_returned(context, user):
    assert await get_user_permissions(context, user)


@pytest.mark.asyncio
async def test_user_without_admin_permission(context, user):
    perms = await get_user_permissions(context, user)
    assert CorePermission.ADMIN not in perms["core"]


@pytest.mark.asyncio
async def test_user_with_admin_permission_from_group(context, user, members, admins):
    user = await user.update_groups(members, [admins])
    perms = await get_user_permissions(context, user)
    assert CorePermission.ADMIN in perms["core"]


@pytest.mark.asyncio
async def test_user_with_admin_permission_from_user(context, user):
    user = await user.update(is_admin=True)
    perms = await get_user_permissions(context, user)
    assert CorePermission.ADMIN in perms["core"]


@pytest.mark.asyncio
async def test_user_without_moderator_permission(context, user):
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
async def test_user_with_moderator_permission_from_user(context, user):
    user = await user.update(is_moderator=True)
    perms = await get_user_permissions(context, user)
    assert CorePermission.MODERATOR in perms["core"]


@pytest.mark.asyncio
async def test_user_is_missing_other_group_core_permission(context, user, admins):
    await permissions_query.insert(group_id=admins.id, permission="TEST_PERM")
    perms = await get_user_permissions(context, user)
    assert "TEST_PERM" not in perms["core"]


@pytest.mark.asyncio
async def test_user_has_core_permission_from_primary_group(context, user, members):
    await permissions_query.insert(group_id=members.id, permission="TEST_PERM")
    perms = await get_user_permissions(context, user)
    assert "TEST_PERM" in perms["core"]


@pytest.mark.asyncio
async def test_user_has_core_permission_from_secondary_group(
    context, user, members, admins
):
    await permissions_query.insert(group_id=admins.id, permission="TEST_PERM")
    user = await user.update_groups(members, [admins])
    perms = await get_user_permissions(context, user)
    assert "TEST_PERM" in perms["core"]


@pytest.mark.asyncio
async def test_user_is_missing_other_group_category_permission(
    context, user, admins, category
):
    await categories_permissions_query.insert(
        category_id=category.id,
        group_id=admins.id,
        permission=CategoryPermission.SEE,
    )

    perms = await get_user_permissions(context, user)
    assert category.id not in perms["category"][CategoryPermission.SEE]


@pytest.mark.asyncio
async def test_user_has_category_permission_from_primary_group(
    context, user, members, category
):
    await categories_permissions_query.insert(
        category_id=category.id,
        group_id=members.id,
        permission=CategoryPermission.SEE,
    )

    perms = await get_user_permissions(context, user)
    assert category.id in perms["category"][CategoryPermission.SEE]


@pytest.mark.asyncio
async def test_user_has_category_permission_from_secondary_group(
    context, user, admins, members, category
):
    await categories_permissions_query.insert(
        category_id=category.id,
        group_id=admins.id,
        permission=CategoryPermission.SEE,
    )

    user = await user.update_groups(members, [admins])
    perms = await get_user_permissions(context, user)
    assert category.id in perms["category"][CategoryPermission.SEE]
