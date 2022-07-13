import pytest


@pytest.mark.asyncio
async def test_user_main_group_is_changed(user, members, admins):
    user_acl_key = user.acl_key
    assert user.group_id == members.id

    updated_user = await user.update_groups(admins, [])
    assert updated_user.group_id == admins.id
    assert updated_user.acl_key != user_acl_key

    assert await updated_user.get_groups() == [admins]


@pytest.mark.asyncio
async def test_user_secondary_group_is_updated(user, members, admins):
    user_acl_key = user.acl_key
    assert user.group_id == members.id

    updated_user = await user.update_groups(members, [admins])
    assert updated_user.group_id == members.id
    assert updated_user.acl_key != user_acl_key

    assert await updated_user.get_groups() == [members, admins]


@pytest.mark.asyncio
async def test_user_secondary_group_is_removed(user, members, admins):
    user_acl_key = user.acl_key
    user = await user.update_groups(members, [admins])
    assert user.group_id == members.id

    updated_user = await user.update_groups(members, [])
    assert updated_user.group_id == members.id
    assert updated_user.acl_key == user_acl_key

    assert await updated_user.get_groups() == [members]
