import pytest

from ....tables import users
from ....users.models import User
from ..registry import MapperRegistry

mapper_registry = MapperRegistry()
mapper_registry.set_mapping(users, User)
users_query = mapper_registry.query_table(users)


@pytest.mark.asyncio
async def test_results_are_filtered_using_or(user, admin):
    results = (
        await users_query.or_filter(id=user.id)
        .or_filter(id=admin.id)
        .order_by("name")
        .all()
    )
    assert results == [admin, user]


@pytest.mark.asyncio
async def test_results_are_filtered_using_filter_and_or(user, admin, inactive_user):
    results = (
        await users_query.exclude(is_active=False)
        .or_filter(id=inactive_user.id)
        .or_filter(id=user.id)
        .or_filter(id=admin.id)
        .order_by("name")
        .all()
    )
    assert results == [admin, user]
