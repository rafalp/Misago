from ...permissions.permissionsid import get_permissions_id
from ..tasks import remove_group_from_users_groups_ids


def test_remove_group_from_users_groups_ids_task_removes_group_from_user_groups_ids(
    user, members_group, custom_group
):
    user.set_groups(members_group, [custom_group])
    user.save()

    remove_group_from_users_groups_ids(custom_group.id)

    user.refresh_from_db()
    assert user.groups_ids == [members_group.id]


def test_remove_group_from_users_groups_ids_task_updates_user_permissions_id(
    user, members_group, custom_group
):
    user.set_groups(members_group, [custom_group])
    user.save()

    remove_group_from_users_groups_ids(custom_group.id)

    user.refresh_from_db()
    assert user.permissions_id == get_permissions_id([members_group.id])
