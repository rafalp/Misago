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
async def test_all_objects_can_be_retrieved_as_named_tuples(admin):
    results = await mapper.query_table(users).all("id", "email", named=True)
    assert len(results) == 1
    assert results[0].id == admin.id
    assert results[0].email == admin.email
    assert (admin.id, admin.email) in results


@pytest.mark.asyncio
async def test_all_objects_can_be_retrieved_as_tuples(user, admin):
    results = await mapper.query_table(users).all("id", "email")
    assert len(results) == 2
    assert (admin.id, admin.email) in results
    assert (user.id, user.email) in results


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
async def test_filtered_objects_can_be_counted(user, admin):
    results = await mapper.query_table(users).filter(is_admin=True).count()
    assert results == 1


@pytest.mark.asyncio
async def test_excluded_objects_can_be_counted(user, admin):
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


@pytest.mark.asyncio
async def test_results_can_be_ordered(user, admin):
    results = await mapper.query_table(users).order_by("name").all()
    assert results == [admin, user]


@pytest.mark.asyncio
async def test_results_can_be_reverse_ordered(user, admin):
    results = await mapper.query_table(users).order_by("-name").all()
    assert results == [user, admin]


@pytest.mark.asyncio
async def test_results_can_be_limited(user, admin):
    results = await mapper.query_table(users).order_by("name").limit(1).all()
    assert results == [admin]


@pytest.mark.asyncio
async def test_results_can_be_offset(user, admin):
    results = await mapper.query_table(users).order_by("name").offset(1).all()
    assert results == [user]


@pytest.mark.asyncio
async def test_results_can_be_offset_limited(user, admin):
    results = await mapper.query_table(users).order_by("name").offset(1).limit(1).all()
    assert results == [user]
