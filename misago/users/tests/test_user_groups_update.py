import pytest


@pytest.mark.asyncio
async def test_user_main_group_is_changed(user, members, admins):
    user_perms_id = user.perms_id
    assert user.group_id == members.id
    assert user.groups_ids == [members.id]

    updated_user = await user.update_groups(admins, [])
    assert updated_user.group_id == admins.id
    assert updated_user.groups_ids == [admins.id]
    assert updated_user.perms_id != user_perms_id

    assert await updated_user.get_groups() == [admins]


@pytest.mark.asyncio
async def test_user_secondary_group_is_updated(user, members, admins):
    user_perms_id = user.perms_id
    assert user.group_id == members.id
    assert user.groups_ids == [members.id]

    updated_user = await user.update_groups(members, [admins])
    assert updated_user.group_id == members.id
    assert updated_user.groups_ids == sorted([members.id, admins.id])
    assert updated_user.perms_id != user_perms_id

    assert await updated_user.get_groups() == [members, admins]


@pytest.mark.asyncio
async def test_user_secondary_group_is_removed(user, members, admins):
    user_perms_id = user.perms_id
    user = await user.update_groups(members, [admins])
    assert user.group_id == members.id
    assert user.groups_ids == sorted([members.id, admins.id])

    updated_user = await user.update_groups(members, [])
    assert updated_user.group_id == members.id
    assert updated_user.groups_ids == [members.id]
    assert updated_user.perms_id == user_perms_id

    assert await updated_user.get_groups() == [members]
