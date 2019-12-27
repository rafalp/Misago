import pytest

from ..users import (
    clear_all_users,
    clear_user,
    clear_users,
    load_user,
    load_users,
    store_user,
    store_users,
)


@pytest.mark.asyncio
async def test_user_loader_returns_user(user):
    loaded_user = await load_user({}, user.id)
    assert loaded_user == user


@pytest.mark.asyncio
async def test_user_loader_returns_none_for_nonexistent_user_id(db):
    loaded_user = await load_user({}, 1)
    assert loaded_user is None


@pytest.mark.asyncio
async def test_users_loader_returns_multiple_users(user, other_user):
    loaded_users = await load_users({}, [user.id, other_user.id])
    assert loaded_users == [user, other_user]


@pytest.mark.asyncio
async def test_users_loader_returns_none_for_nonexistent_user_id(user):
    loaded_users = await load_users({}, [user.id, user.id + 1])
    assert loaded_users == [user, None]


@pytest.mark.asyncio
async def test_user_is_stored_in_loader_for_future_use(user):
    context = {}
    store_user(context, user)
    loaded_user = await load_user(context, user.id)
    assert id(loaded_user) == id(user)


@pytest.mark.asyncio
async def test_users_are_stored_in_loader_for_future_use(user):
    context = {}
    store_users(context, [user])
    loaded_user = await load_user(context, user.id)
    assert id(loaded_user) == id(user)


@pytest.mark.asyncio
async def test_user_is_cleared_from_loader(user):
    context = {}
    loaded_user = await load_user(context, user.id)
    clear_user(context, user)
    new_loaded_user = await load_user(context, user.id)
    assert id(loaded_user) != id(new_loaded_user)


@pytest.mark.asyncio
async def test_users_are_cleared_from_loader(user):
    context = {}
    loaded_user = await load_user(context, user.id)
    clear_users(context, [user])
    new_loaded_user = await load_user(context, user.id)
    assert id(loaded_user) != id(new_loaded_user)


@pytest.mark.asyncio
async def test_all_users_are_cleared_from_loader(user):
    context = {}
    loaded_user = await load_user(context, user.id)
    clear_all_users(context)
    new_loaded_user = await load_user(context, user.id)
    assert id(loaded_user) != id(new_loaded_user)
