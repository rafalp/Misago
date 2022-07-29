import pytest

from ...tables import posts, threads, users
from ...threads.models import Post
from ...users.models import User
from ..objectmapper2 import InvalidColumnError, InvalidJoinError, ObjectMapper

mapper = ObjectMapper()

mapper.set_mapping(posts, Post)
mapper.set_mapping(users, User)


@pytest.mark.asyncio
async def test_objects_can_be_filtered_with_subquery(
    admin, user, user_thread, user_post
):
    subquery = mapper.query_table(users).filter(is_admin=False).subquery()
    results = await mapper.query_table(posts).filter(poster_id__in=subquery).all()
    assert results == [user_post]


@pytest.mark.asyncio
async def test_objects_can_be_excluded_with_subquery(
    admin, user, user_thread, user_post
):
    subquery = mapper.query_table(users).exclude(is_admin=True).subquery("id")
    results = await mapper.query_table(posts).filter(poster_id__in=subquery).all()
    assert results == [user_post]


@pytest.mark.asyncio
async def test_subquery_can_use_explicit_return_value(
    admin, user, user_thread, user_post
):
    subquery = mapper.query_table(users).exclude(is_admin=True).subquery("id")
    results = await mapper.query_table(posts).filter(poster_id__in=subquery).all()
    assert results == [user_post]


@pytest.mark.asyncio
async def test_subquery_can_use_joins(admin, user, user_thread, user_post):
    subquery = (
        mapper.query_table(threads).join_on("starter_id").subquery("starter_id.id")
    )
    results = await mapper.query_table(posts).filter(poster_id__in=subquery).all()
    assert results == [user_post]


@pytest.mark.asyncio
async def test_subquery_raises_error_if_column_is_invalid(db):
    with pytest.raises(InvalidColumnError):
        mapper.query_table(threads).subquery("invalid")


@pytest.mark.asyncio
async def test_subquery_raises_error_if_join_is_invalid(db):
    with pytest.raises(InvalidJoinError):
        mapper.query_table(threads).subquery("invalid.id")
