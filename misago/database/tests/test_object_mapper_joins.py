import pytest

from ...tables import (
    users,
    user_group_memberships,
    user_groups,
)
from ...users.models import User, UserGroup
from ..objectmapper2 import ObjectMapper

mapper = ObjectMapper()

mapper.set_mapping(users, User)
mapper.set_mapping(user_groups, UserGroup)


@pytest.mark.asyncio
async def test_all_objects_can_be_retrieved_with_singe_join(
    user, admin, admins, members
):
    results = await mapper.query_table(users).join_on("group_id").all()
    assert len(results) == 2
    for member, group in results:
        assert member.group_id == group.id


@pytest.mark.asyncio
async def test_all_objects_can_be_retrieved_with_multiple_joins(
    user, admin, moderator, admins, moderators, members
):
    results = (
        await mapper.query_table(user_group_memberships)
        .join_on("user_id", "group_id")
        .all()
    )
    assert len(results) == 3
    for membership, member, group in results:
        assert membership["user_id"] == member.id
        assert membership["group_id"] == group.id
