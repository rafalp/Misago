import pytest

from ...users.get import get_users_by_id
from ...users.models import User
from ..loader import Loader
from ..batchloadfunction import BatchLoadFunction, batch_load_function

batch_load_users = batch_load_function(get_users_by_id)


class UsersLoader(Loader[User]):
    context_key = "user_loader"

    def get_batch_load_function(self) -> BatchLoadFunction:
        return batch_load_users


@pytest.fixture
def loader(db):
    return UsersLoader()


@pytest.fixture
def context(loader):
    c = {}
    loader.setup_context(c)
    return c


@pytest.mark.asyncio
async def test_loader_loads_object_by_id(context, loader, user):
    loaded_obj = await loader.load(context, user.id)
    assert loaded_obj == user


@pytest.mark.asyncio
async def test_loader_returns_none_if_obj_with_id_is_not_found(context, loader):
    loaded_obj = await loader.load(context, 1)
    assert loaded_obj is None


@pytest.mark.asyncio
async def test_loader_loads_multiple_objects(context, loader, user, admin):
    loaded_objects = await loader.load_many(context, [user.id, admin.id])
    assert loaded_objects == [user, admin]


@pytest.mark.asyncio
async def test_loader_returns_none_for_not_found_objects(context, loader, user):
    loaded_objects = await loader.load_many(context, [user.id, user.id + 1])
    assert loaded_objects == [user, None]


@pytest.mark.asyncio
async def test_object_is_stored_in_loader_for_future_use(context, loader, user):
    loader.store(context, user)
    loaded_obj = await loader.load(context, user.id)
    assert loaded_obj == user


@pytest.mark.asyncio
async def test_stored_object_replaces_previous_one(context, loader, user):
    loader.store(context, user)

    updated_object = await user.update(name="Updated")
    loader.store(context, updated_object)

    loaded_object = await loader.load(context, user.id)
    assert loaded_object == updated_object


@pytest.mark.asyncio
async def test_multiple_objects_are_stored_in_loader_for_future_use(
    context, loader, user, admin
):
    loader.store_many(context, [user, admin])
    loaded_objects = await loader.load_many(context, [user.id, admin.id])
    assert loaded_objects == [user, admin]


@pytest.mark.asyncio
async def test_object_is_unloaded_from_loader(context, loader, user):
    loaded_obj = await loader.load(context, user.id)
    assert loaded_obj == user

    updated_obj = await user.update(name="Changed")
    loaded_obj = await loader.load(context, user.id)
    assert loaded_obj != updated_obj

    loader.unload(context, user.id)
    loaded_obj = await loader.load(context, user.id)
    assert loaded_obj == updated_obj


@pytest.mark.asyncio
async def test_multiple_objects_are_unloaded_from_loader(context, loader, user, admin):
    loaded_obj, other_loaded_obj = await loader.load_many(context, [user.id, admin.id])
    assert loaded_obj == user
    assert other_loaded_obj == admin

    updated_obj = await loaded_obj.update(name="Updated")
    other_updated_obj = await other_loaded_obj.update(name="UpdatedToo")

    loaded_obj = await loader.load(context, user.id)
    assert loaded_obj != updated_obj

    loader.unload_many(context, [user.id, admin.id])

    loaded_obj = await loader.load(context, user.id)
    assert loaded_obj == updated_obj

    other_loaded_obj = await loader.load(context, admin.id)
    assert other_loaded_obj == other_updated_obj


@pytest.mark.asyncio
async def test_object_is_unloaded_from_loader_by_attr_value(
    context, loader, user, admin
):
    loaded_obj, other_loaded_obj = await loader.load_many(context, [user.id, admin.id])
    assert loaded_obj == user
    assert other_loaded_obj == admin

    updated_obj = await loaded_obj.update(name="Updated")
    other_updated_obj = await other_loaded_obj.update(name="UpdatedToo")

    loaded_obj = await loader.load(context, user.id)
    assert loaded_obj != updated_obj

    loader.unload_by_attr_value(context, "email", user.email)
    loaded_obj = await loader.load(context, user.id)
    assert loaded_obj == updated_obj

    other_loaded_obj = await loader.load(context, admin.id)
    assert other_loaded_obj != other_updated_obj


@pytest.mark.asyncio
async def test_object_is_unloaded_from_loader_by_attr_values(
    context, loader, user, admin
):
    loaded_obj, other_loaded_obj = await loader.load_many(context, [user.id, admin.id])
    assert loaded_obj == user
    assert other_loaded_obj == admin

    updated_obj = await loaded_obj.update(name="Updated")
    other_updated_obj = await other_loaded_obj.update(name="UpdatedToo")

    loaded_obj = await loader.load(context, user.id)
    assert loaded_obj != updated_obj

    loader.unload_by_attr_value_in(context, "email", [user.email, admin.email])
    loaded_obj = await loader.load(context, user.id)
    assert loaded_obj == updated_obj

    other_loaded_obj = await loader.load(context, admin.id)
    assert other_loaded_obj == other_updated_obj


@pytest.mark.asyncio
async def test_all_objects_are_unloaded_from_loader(context, loader, user):
    loaded_obj = await loader.load(context, user.id)
    assert loaded_obj == user

    updated_obj = await user.update(name="Changed")
    loaded_obj = await loader.load(context, user.id)
    assert loaded_obj != updated_obj

    loader.unload_all(context)
    loaded_obj = await loader.load(context, user.id)
    assert loaded_obj == updated_obj
