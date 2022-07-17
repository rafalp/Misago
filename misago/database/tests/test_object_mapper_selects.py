import pytest

from ...tables import users, user_groups
from ...users.models import User, UserGroup
from ..objectmapper2 import ObjectMapper

mapper = ObjectMapper()

mapper.set_mapping(users, User)
mapper.set_mapping(user_groups, UserGroup)


@pytest.mark.asyncio
async def test_all_objects_can_be_retrieved(user, admin):
    results = await mapper.query_table(users).all()
    assert len(results) == 2
    assert admin in results
    assert user in results


@pytest.mark.asyncio
async def test_no_objects_can_be_retrieved(db):
    results = await mapper.query_table(users).all()
    assert results == []


@pytest.mark.asyncio
async def test_filtered_objects_can_be_retrieved(user, admin):
    results = await mapper.query_table(users).filter(is_admin=True).all()
    assert results == [admin]


@pytest.mark.asyncio
async def test_excluded_objects_can_be_retrieved(user, admin):
    results = await mapper.query_table(users).exclude(is_admin=True).all()
    assert results == [user]


@pytest.mark.asyncio
async def test_all_objects_can_be_counted(user, admin):
    result = await mapper.query_table(users).count()
    assert result == 2


@pytest.mark.asyncio
async def test_no_objects_can_be_counted(db):
    result = await mapper.query_table(users).count()
    assert result == 0


@pytest.mark.asyncio
async def test_filtered_objects_can_be_counter(user, admin):
    results = await mapper.query_table(users).filter(is_admin=True).count()
    assert results == 1


@pytest.mark.asyncio
async def test_excluded_objects_can_be_counter(user, admin):
    results = await mapper.query_table(users).exclude(is_admin=True).count()
    assert results == 1


@pytest.mark.asyncio
async def test_all_objects_existence_can_be_tested(user, admin):
    result = await mapper.query_table(users).exists()
    assert result is True


@pytest.mark.asyncio
async def test_all_objects_non_existence_can_be_tested(db):
    result = await mapper.query_table(users).exists()
    assert result is False


@pytest.mark.asyncio
async def test_filtered_objects_can_be_tested(user, admin):
    result = await mapper.query_table(users).filter(is_admin=True).exists()
    assert result is True

    result = (
        await mapper.query_table(users)
        .filter(is_admin=True, is_moderator=True)
        .exists()
    )
    assert result is False


@pytest.mark.asyncio
async def test_excluded_objects_can_be_tested(user, admin):
    result = await mapper.query_table(users).exclude(is_admin=True).exists()
    assert result is True

    result = (
        await mapper.query_table(users)
        .exclude(is_admin=True, is_moderator=False)
        .exists()
    )
    assert result is False
