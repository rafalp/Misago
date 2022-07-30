import pytest

from ....tables import users
from ....users.models import User
from ..exceptions import InvalidColumnError
from ..registry import MapperRegistry

mapper_registry = MapperRegistry()
mapper_registry.set_mapping(users, User)
root_query = mapper_registry.query_table(users)


@pytest.mark.asyncio
async def test_all_rows_can_be_updated(user):
    await root_query.update_all(email="updated@email.com")

    user_from_db = await user.fetch_from_db()
    assert user_from_db.email == "updated@email.com"


@pytest.mark.asyncio
async def test_update_raises_error_on_root_query(db):
    with pytest.raises(NotImplementedError):
        await root_query.update(email="updated@email.com")


@pytest.mark.asyncio
async def test_filtered_rows_can_be_updated(user, admin):
    await root_query.filter(is_admin=False).update(email="updated@email.com")

    user_from_db = await user.fetch_from_db()
    assert user_from_db.email == "updated@email.com"

    admin_from_db = await admin.fetch_from_db()
    assert admin_from_db.email == admin.email


@pytest.mark.asyncio
async def test_update_raises_error_if_column_name_is_invalid(db):
    with pytest.raises(InvalidColumnError):
        await root_query.filter(is_admin=False).update(invalid="updated@email.com")
