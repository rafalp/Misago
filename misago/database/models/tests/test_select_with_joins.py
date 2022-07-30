import pytest

from ....tables import (
    threads,
    posts,
    users,
    user_group_memberships,
    user_groups,
)
from ....threads.models import Post, Thread
from ....users.models import User, UserGroup
from ..exceptions import InvalidColumnError, InvalidJoinError
from ..registry import MapperRegistry

mapper_registry = MapperRegistry()

mapper_registry.set_mapping(posts, Post)
mapper_registry.set_mapping(threads, Thread)
mapper_registry.set_mapping(users, User)
mapper_registry.set_mapping(user_groups, UserGroup)


@pytest.mark.asyncio
async def test_all_objects_can_be_retrieved_with_single_join(
    user, admin, admins, members
):
    results = await mapper_registry.query_table(users).join_on("group_id").all()
    assert len(results) == 2
    for member, group in results:
        assert member in (user, admin)
        assert group in (admins, members)
        assert member.group_id == group.id


@pytest.mark.asyncio
async def test_all_objects_can_be_retrieved_with_single_join_missing_relation(thread):
    results = await mapper_registry.query_table(threads).join_on("starter_id").all()
    assert results == [(thread, None)]


@pytest.mark.asyncio
async def test_all_objects_can_be_retrieved_with_deep_joins(
    user_thread, user_post, user
):
    results = (
        await mapper_registry.query_table(threads)
        .join_on("first_post_id.poster_id")
        .all()
    )
    assert results == [(user_thread, user)]


@pytest.mark.asyncio
async def test_all_objects_can_be_retrieved_with_deep_joins_missing_relation(
    thread, post, user
):
    results = (
        await mapper_registry.query_table(threads)
        .join_on("first_post_id.poster_id")
        .all()
    )
    assert results == [(thread, None)]


@pytest.mark.asyncio
async def test_all_objects_can_be_retrieved_with_deep_and_shallow_joins(
    user_thread, user_post, user
):
    results = (
        await mapper_registry.query_table(threads)
        .join_on("first_post_id", "first_post_id.poster_id")
        .all()
    )
    assert results == [(user_thread, user_post, user)]


@pytest.mark.asyncio
async def test_all_objects_can_be_retrieved_with_reversed_deep_and_shallow_joins(
    user_thread, user_post, user
):
    results = (
        await mapper_registry.query_table(threads)
        .join_on("first_post_id.poster_id", "first_post_id")
        .all()
    )
    assert results == [(user_thread, user, user_post)]


@pytest.mark.asyncio
async def test_all_objects_can_be_retrieved_with_multiple_joins(
    user, admin, moderator, admins, moderators, members
):
    results = (
        await mapper_registry.query_table(user_group_memberships)
        .join_on("user_id", "group_id")
        .all()
    )
    assert len(results) == 3
    for m, u, g in results:
        assert u in (user, admin, moderator)
        assert g in (members, admins, moderator)
        assert m == {
            "id": m["id"],
            "is_main": True,
            "user_id": u.id,
            "group_id": g.id,
        }


@pytest.mark.asyncio
async def test_join_raises_error_if_column_to_join_on_doesnt_exist(db):
    with pytest.raises(InvalidColumnError):
        await mapper_registry.query_table(users).join_on("invalid")


@pytest.mark.asyncio
async def test_join_raises_error_if_relation_column_to_join_on_doesnt_exist(db):
    with pytest.raises(InvalidColumnError):
        await mapper_registry.query_table(users).join_on("group_id.invalid")


@pytest.mark.asyncio
async def test_joins_can_be_filtered(user, admin, admins, members):
    results = (
        await mapper_registry.query_table(users)
        .join_on("group_id")
        .filter(is_admin=True)
        .all()
    )
    assert results == [(admin, admins)]


@pytest.mark.asyncio
async def test_joins_can_be_filtered_over_relation(user, admin, admins, members):
    results = (
        await mapper_registry.query_table(users)
        .join_on("group_id")
        .filter(**{"group_id.is_admin": True})
        .all()
    )
    assert results == [(admin, admins)]


@pytest.mark.asyncio
async def test_select_raises_invalid_join_error_if_filtered_over_missing_join(db):
    with pytest.raises(InvalidJoinError):
        await mapper_registry.query_table(users).filter(
            **{"not_join.is_admin": True}
        ).all()


@pytest.mark.asyncio
async def test_joins_can_be_ordered(user, admin, admins, members):
    results = (
        await mapper_registry.query_table(users)
        .join_on("group_id")
        .order_by("name")
        .all()
    )
    assert results == [(admin, admins), (user, members)]


@pytest.mark.asyncio
async def test_joins_can_be_limited(user, admin, admins, members):
    results = (
        await mapper_registry.query_table(users)
        .join_on("group_id")
        .order_by("name")
        .limit(1)
        .all()
    )
    assert results == [(admin, admins)]


@pytest.mark.asyncio
async def test_joins_can_be_offset(user, admin, admins, members):
    results = (
        await mapper_registry.query_table(users)
        .join_on("group_id")
        .order_by("name")
        .offset(1)
        .all()
    )
    assert results == [(user, members)]


@pytest.mark.asyncio
async def test_joins_can_be_counted(user, admin, admins, members):
    result = (
        await mapper_registry.query_table(users)
        .join_on("group_id")
        .order_by("name")
        .count()
    )
    assert result == 2


@pytest.mark.asyncio
async def test_joins_can_be_tested_for_existence(user, admin, admins, members):
    result = (
        await mapper_registry.query_table(users)
        .join_on("group_id")
        .order_by("name")
        .exists()
    )
    assert result is True


@pytest.mark.asyncio
async def test_joins_can_be_offset_limited(user, admin, admins, members):
    results = (
        await mapper_registry.query_table(users)
        .join_on("group_id")
        .order_by("name")
        .offset(1)
        .limit(1)
        .all()
    )
    assert results == [(user, members)]


@pytest.mark.asyncio
async def test_joins_can_be_retrieved_as_named_tuples(user, members):
    results = (
        await mapper_registry.query_table(users)
        .join_on("group_id")
        .all("id", "email", "group_id.id", "group_id.name", named=True)
    )
    assert len(results) == 1
    assert len(results[0]) == 2
    assert results[0][0].id == user.id
    assert results[0][0].email == user.email


@pytest.mark.asyncio
async def test_joins_can_be_retrieved_as_named_tuples_without_primary_keys(
    user, members
):
    results = (
        await mapper_registry.query_table(users)
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
        await mapper_registry.query_table(threads)
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
        await mapper_registry.query_table(users)
        .join_on("group_id")
        .all("id", "email", "group_id.name")
    )
    assert len(results) == 2
    assert (admin.id, admin.email, admins.name) in results
    assert (user.id, user.email, members.name) in results


@pytest.mark.asyncio
async def test_join_raises_error_if_column_name_is_invalid(db):
    with pytest.raises(InvalidColumnError):
        await mapper_registry.query_table(users).join_on("group_id").all("invalid")

    with pytest.raises(InvalidColumnError):
        await mapper_registry.query_table(users).join_on("group_id").all(
            "invalid", named=True
        )


@pytest.mark.asyncio
async def test_join_raises_error_if_relation_column_name_is_invalid(db):
    with pytest.raises(InvalidColumnError):
        await mapper_registry.query_table(users).join_on("group_id").all(
            "group_id.invalid"
        )

    with pytest.raises(InvalidColumnError):
        await mapper_registry.query_table(users).join_on("group_id").all(
            "group_id.invalid", named=True
        )
