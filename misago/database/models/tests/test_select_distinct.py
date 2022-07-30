import pytest

from ....tables import users, user_groups
from ....users.models import User, UserGroup
from ..registry import MapperRegistry

mapper_registry = MapperRegistry()

mapper_registry.set_mapping(users, User)
mapper_registry.set_mapping(user_groups, UserGroup)

users_query = mapper_registry.query_table(users)
groups_query = mapper_registry.query_table(user_groups)


@pytest.mark.asyncio
async def test_distinct_values_can_be_selected_from_simple_query(
    user, admin, moderator, admins, members
):
    user_ids = await users_query.distinct().all_flat("id")
    assert len(user_ids) == 3
    assert user.id in user_ids
    assert admin.id in user_ids
    assert moderator.id in user_ids

    moderators = await users_query.distinct().all_flat("is_moderator")
    assert len(moderators) == 2
    assert True in moderators
    assert False in moderators


@pytest.mark.asyncio
async def test_distinct_values_can_be_selected_from_query_with_join(
    user, admin, admins, members
):
    groups_ids = await users_query.join_on("group_id").all_flat("group_id")
    assert len(groups_ids) == 2
    assert admins.id in groups_ids
    assert members.id in groups_ids
