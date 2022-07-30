import pytest

from ....tables import users
from ....users.models import User
from ..registry import MapperRegistry

mapper_registry = MapperRegistry()
mapper_registry.set_mapping(users, User)
root_query = mapper_registry.query_table(users)


@pytest.mark.asyncio
async def test_all_objects_can_be_deleted(user, admin):
    await root_query.delete_all()

    count = await root_query.count()
    assert count == 0


@pytest.mark.asyncio
async def test_all_objects_cant_be_deleted_on_filtered_query(user, admin):
    with pytest.raises(NotImplementedError):
        await root_query.filter(is_admin=True).delete_all()


@pytest.mark.asyncio
async def test_selected_objects_can_be_deleted(user, admin):
    org_count = await root_query.count()
    await root_query.filter(is_admin=True).delete()

    new_count = await root_query.count()
    assert org_count - 1 == new_count


@pytest.mark.asyncio
async def test_selected_objects_cant_be_deleted_on_root_query(user, admin):
    with pytest.raises(NotImplementedError):
        await root_query.delete()
