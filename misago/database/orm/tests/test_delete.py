import pytest

from ....tables import users
from ....users.models import User
from ..mapper import ObjectMapper

mapper = ObjectMapper()
mapper.set_mapping(users, User)


@pytest.mark.asyncio
async def test_all_objects_can_be_deleted(user, admin):
    await mapper.query_table(users).delete_all()

    count = await mapper.query_table(users).count()
    assert count == 0


@pytest.mark.asyncio
async def test_all_objects_cant_be_deleted_on_filtered_query(user, admin):
    with pytest.raises(NotImplementedError):
        await mapper.query_table(users).filter(is_admin=True).delete_all()


@pytest.mark.asyncio
async def test_selected_objects_can_be_deleted(user, admin):
    org_count = await mapper.query_table(users).count()
    await mapper.query_table(users).filter(is_admin=True).delete()

    new_count = await mapper.query_table(users).count()
    assert org_count - 1 == new_count


@pytest.mark.asyncio
async def test_selected_objects_cant_be_deleted_on_root_query(user, admin):
    with pytest.raises(NotImplementedError):
        await mapper.query_table(users).delete()
