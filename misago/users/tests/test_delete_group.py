from unittest.mock import patch

import pytest

from ..groups import delete_group
from ..models import Group


@patch("misago.users.groups.remove_group_from_users_groups_ids")
def test_delete_group_deletes_group_with_its_relations(
    mock_remove_group_from_users_groups_ids, members_group
):
    delete_group(members_group)

    with pytest.raises(Group.DoesNotExist):
        members_group.refresh_from_db()


@patch("misago.users.groups.remove_group_from_users_groups_ids")
def test_delete_group_calls_cleanup_task(
    mock_remove_group_from_users_groups_ids, members_group
):
    delete_group(members_group)

    mock_remove_group_from_users_groups_ids.delay.assert_called_once_with(
        members_group.id
    )
