import pytest

from ...tables import (
    threads,
    posts,
    users,
    user_group_memberships,
    user_groups,
)
from ...threads.models import Post, Thread
from ...users.models import User, UserGroup
from ..objectmapper2 import InvalidColumnError, ObjectMapper

mapper = ObjectMapper()

mapper.set_mapping(posts, Post)
mapper.set_mapping(threads, Thread)
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
async def test_all_objects_can_be_retrieved_with_deep_joins(
    user_thread, user_post, user
):
    results = await mapper.query_table(threads).join_on("first_post_id.poster_id").all()

    results_ids = []
    for thread, user in results:
        results_ids.append((thread.id, user.id))

    assert results_ids == [(user_thread.id, user.id)]


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


@pytest.mark.asyncio
async def test_join_raises_error_if_column_to_use_doesnt_exist(db):
    with pytest.raises(InvalidColumnError):
        await mapper.query_table(users).join_on("invalid")


@pytest.mark.asyncio
async def test_joins_can_be_filtered(user, admin, admins, members):
    results = (
        await mapper.query_table(users).join_on("group_id").filter(is_admin=True).all()
    )
    results == [(admin, admins)]
