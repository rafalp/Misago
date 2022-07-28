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
async def test_all_objects_can_be_retrieved_with_single_join(
    user, admin, admins, members
):
    results = await mapper.query_table(users).join_on("group_id").all()
    assert len(results) == 2
    for member, group in results:
        assert member.group_id == group.id


@pytest.mark.asyncio
async def test_all_objects_can_be_retrieved_with_single_join_missing_relation(thread):
    results = await mapper.query_table(threads).join_on("starter_id").all()
    assert len(results) == 1
    for t, s in results:
        assert t.starter_id is None
        assert s is None


@pytest.mark.asyncio
async def test_all_objects_can_be_retrieved_with_deep_joins(
    user_thread, user_post, user
):
    results = await mapper.query_table(threads).join_on("first_post_id.poster_id").all()

    results_ids = []
    for t, u in results:
        results_ids.append((t.id, u.id))

    assert results_ids == [(user_thread.id, user.id)]


@pytest.mark.asyncio
async def test_all_objects_can_be_retrieved_with_deep_joins_missing_relation(
    thread, post, user
):
    results = await mapper.query_table(threads).join_on("first_post_id.poster_id").all()

    results_ids = []
    for t, u in results:
        results_ids.append((t.id, u))

    assert results_ids == [(thread.id, None)]


@pytest.mark.asyncio
async def test_all_objects_can_be_retrieved_with_deep_and_shallow_joins(
    user_thread, user_post, user
):
    results = (
        await mapper.query_table(threads)
        .join_on("first_post_id", "first_post_id.poster_id")
        .all()
    )

    results_ids = []
    for t, p, u in results:
        results_ids.append((t.id, p.id, u.id))

    assert results_ids == [(user_thread.id, user_post.id, user.id)]


@pytest.mark.asyncio
async def test_all_objects_can_be_retrieved_with_reversed_deep_and_shallow_joins(
    user_thread, user_post, user
):
    results = (
        await mapper.query_table(threads)
        .join_on("first_post_id.poster_id", "first_post_id")
        .all()
    )

    results_ids = []
    for t, u, p in results:
        results_ids.append((t.id, u.id, p.id))

    assert results_ids == [(user_thread.id, user.id, user_post.id)]


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
    for m, u, g in results:
        assert m["user_id"] == u.id
        assert m["group_id"] == g.id


@pytest.mark.asyncio
async def test_join_raises_error_if_column_to_join_on_doesnt_exist(db):
    with pytest.raises(InvalidColumnError):
        await mapper.query_table(users).join_on("invalid")


@pytest.mark.asyncio
async def test_join_raises_error_if_relation_column_to_join_on_doesnt_exist(db):
    with pytest.raises(InvalidColumnError):
        await mapper.query_table(users).join_on("group_id.invalid")


@pytest.mark.asyncio
async def test_joins_can_be_filtered(user, admin, admins, members):
    results = (
        await mapper.query_table(users).join_on("group_id").filter(is_admin=True).all()
    )
    assert results == [(admin, admins)]


@pytest.mark.asyncio
async def test_joins_can_be_ordered(user, admin, admins, members):
    results = (
        await mapper.query_table(users).join_on("group_id").order_by("is_admin").all()
    )
    assert results == [(admin, admins), (user, members)]


@pytest.mark.asyncio
async def test_joins_can_be_limited(user, admin, admins, members):
    results = (
        await mapper.query_table(users)
        .join_on("group_id")
        .order_by("is_admin")
        .limit(1)
        .all()
    )
    assert results == [(admin, admins)]


@pytest.mark.asyncio
async def test_joins_can_be_offset(user, admin, admins, members):
    results = (
        await mapper.query_table(users)
        .join_on("group_id")
        .order_by("is_admin")
        .offset(1)
        .all()
    )
    assert results == [(user, members)]


@pytest.mark.asyncio
async def test_joins_can_be_offset_limited(user, admin, admins, members):
    results = (
        await mapper.query_table(users)
        .join_on("group_id")
        .order_by("is_admin")
        .offset(1)
        .limit(1)
        .all()
    )
    assert results == [(user, members)]


@pytest.mark.asyncio
async def test_joins_can_be_retrieved_as_named_tuples(user, members):
    results = (
        await mapper.query_table(users)
        .join_on("group_id")
        .all("id", "email", "group_id.id", "group_id.name", named=True)
    )
    assert len(results) == 1
    assert len(results[0]) == 2
    assert results[0][0].id == user.id
    assert results[0][0].email == user.email
    assert results[0][1].id == members.id
    assert results[0][1].name == members.name


@pytest.mark.asyncio
async def test_joins_can_be_retrieved_as_named_tuples_without_primary_keys(
    user, members
):
    results = (
        await mapper.query_table(users)
        .join_on("group_id")
        .all("email", "group_id.name", named=True)
    )
    assert len(results) == 1
    assert len(results[0]) == 2
    assert results[0][0].email == user.email
    assert results[0][1].name == members.name


@pytest.mark.asyncio
async def test_joins_with_missing_relations_can_be_retrieved_as_named_tuples(
    thread,
):
    results = (
        await mapper.query_table(threads)
        .join_on("starter_id")
        .all("id", "title", "starter_id.email", named=True)
    )
    assert len(results) == 1
    assert len(results[0]) == 2
    assert results[0][0].id == thread.id
    assert results[0][0].title == thread.title
    assert results[0][1] is None


@pytest.mark.asyncio
async def test_joins_can_be_retrieved_as_tuples(user, admin, admins, members):
    results = (
        await mapper.query_table(users)
        .join_on("group_id")
        .all("id", "email", "group_id.name")
    )
    assert len(results) == 2
    assert (admin.id, admin.email, admins.name) in results
    assert (user.id, user.email, members.name) in results


@pytest.mark.asyncio
async def test_join_raises_error_if_column_name_is_invalid(db):
    with pytest.raises(InvalidColumnError):
        await mapper.query_table(users).join_on("group_id").all("invalid")

    with pytest.raises(InvalidColumnError):
        await mapper.query_table(users).join_on("group_id").all("invalid", named=True)


@pytest.mark.asyncio
async def test_join_raises_error_if_relation_column_name_is_invalid(db):
    with pytest.raises(InvalidColumnError):
        await mapper.query_table(users).join_on("group_id").all("group_id.invalid")

    with pytest.raises(InvalidColumnError):
        await mapper.query_table(users).join_on("group_id").all(
            "group_id.invalid", named=True
        )
