import pytest

from ...tables import posts, users
from ...threads.models import Post
from ...users.models import User
from ..objectmapper2 import InvalidColumnError, ObjectMapper

mapper = ObjectMapper()

mapper.set_mapping(posts, Post)
mapper.set_mapping(users, User)


@pytest.mark.asyncio
async def test_objects_can_be_filtered_with_subquery(
    admin, user, user_thread, user_post
):
    subquery = mapper.query_table(users).filter(is_admin=False).subquery("id")
    results = await mapper.query_table(posts).filter(poster_id__in=subquery).all()
    assert results == [user_post]


@pytest.mark.asyncio
async def test_objects_can_be_excluded_with_subquery(
    admin, user, user_thread, user_post
):
    subquery = mapper.query_table(users).exclude(is_admin=True).subquery("id")
    results = await mapper.query_table(posts).filter(poster_id__in=subquery).all()
    assert results == [user_post]
