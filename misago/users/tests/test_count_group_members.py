from ..enums import DefaultGroupId
from ..groups import count_groups_members


def test_count_groups_members_returns_all_groups_with_members(
    admin, other_admin, secondary_admin, user
):
    results = count_groups_members()
    results_dict = {group_id: members for group_id, members in results}
    assert results_dict == {
        DefaultGroupId.ADMINS: 3,
        DefaultGroupId.MEMBERS: 2,
    }


def test_count_groups_members_counts_secondary_groups(
    user, members_group, moderators_group
):
    user.set_groups(members_group, [moderators_group])
    user.save()

    results = count_groups_members()
    results_dict = {group_id: members for group_id, members in results}
    assert results_dict == {
        DefaultGroupId.MODERATORS: 1,
        DefaultGroupId.MEMBERS: 1,
    }
