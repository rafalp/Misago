import pytest

from ....tables import posts, users
from ....threads.models import Post
from ....users.models import User
from ..exceptions import DoesNotExist
from ..registry import MapperRegistry

mapper_registry = MapperRegistry()
mapper_registry.set_mapping(posts, Post)
mapper_registry.set_mapping(users, User)

posts_query = mapper_registry.query_table(posts)
users_query = mapper_registry.query_table(users)


@pytest.mark.asyncio
async def test_results_are_filtered_by_equal(admin):
    result = await users_query.filter(id=admin.id).one()
    assert result == admin


@pytest.mark.asyncio
async def test_results_are_filtered_by_greater_than_or_equal(admin):
    result = await users_query.filter(id__gte=admin.id).one()
    assert result == admin

    result = await users_query.filter(id__gte=admin.id - 1).one()
    assert result == admin


@pytest.mark.asyncio
async def test_results_are_filtered_by_less_than_or_equal(admin):
    result = await users_query.filter(id__lte=admin.id).one()
    assert result == admin

    result = await users_query.filter(id__lte=admin.id + 1).one()
    assert result == admin


@pytest.mark.asyncio
async def test_results_are_filtered_by_greater_than(admin):
    with pytest.raises(DoesNotExist):
        await users_query.filter(id__gt=admin.id).one()

    result = await users_query.filter(id__gt=admin.id - 1).one()
    assert result == admin


@pytest.mark.asyncio
async def test_results_are_filtered_by_less_than(admin):
    with pytest.raises(DoesNotExist):
        await users_query.filter(id__lt=admin.id).one()

    result = await users_query.filter(id__lt=admin.id + 1).one()
    assert result == admin


@pytest.mark.asyncio
async def test_results_are_excluded_by_equal(user, admin):
    result = await users_query.exclude(id=user.id).one()
    assert result == admin


@pytest.mark.asyncio
async def test_nulls_are_non_equal_to_value(user_post, post):

    result = await posts_query.exclude(poster_id=user_post.poster_id).one()
    assert result == post


@pytest.mark.asyncio
async def test_values_are_non_equal_to_nulls(user_post, post):
    result = await posts_query.exclude(poster_id=None).one()
    assert result == user_post


@pytest.mark.asyncio
async def test_results_are_excluded_by_greater_than_or_equal(admin):
    with pytest.raises(DoesNotExist):
        await users_query.exclude(id__gte=admin.id).one()

    result = await users_query.exclude(id__gte=admin.id + 1).one()
    assert result == admin


@pytest.mark.asyncio
async def test_results_are_excluded_by_less_than_or_equal(admin):
    with pytest.raises(DoesNotExist):
        await users_query.exclude(id__lte=admin.id).one()

    result = await users_query.exclude(id__lte=admin.id - 1).one()
    assert result == admin


@pytest.mark.asyncio
async def test_results_are_excluded_by_greater_than(admin):
    with pytest.raises(DoesNotExist):
        await users_query.exclude(id__gt=admin.id - 1).one()

    result = await users_query.exclude(id__gt=admin.id).one()
    assert result == admin


@pytest.mark.asyncio
async def test_results_are_excluded_by_less_than(admin):
    with pytest.raises(DoesNotExist):
        await users_query.exclude(id__lt=admin.id + 1).one()

    result = await users_query.exclude(id__lt=admin.id).one()
    assert result == admin
