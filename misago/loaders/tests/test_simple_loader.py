from asyncio import gather

import pytest

from ...users.models import User
from ..simpleloader import simple_loader


@simple_loader("test_loader")
async def load_items(context, **kwargs):
    context.setdefault("hits", 0)
    context["hits"] += 1
    return await User.query.all()


@pytest.mark.asyncio
async def test_simple_loader_loads_data(user, other_user):
    context = {}
    items = await load_items(context)
    assert user in items
    assert other_user in items


@pytest.mark.asyncio
async def test_simple_loader_stores_data_on_context(user, other_user):
    context = {}
    assert await load_items(context)
    assert context


@pytest.mark.asyncio
async def test_simple_loader_reuses_data_from_context(user, other_user):
    context = {}
    result = await load_items(context)
    assert context
    result_2 = await load_items(context)
    assert result == result_2
    assert context["hits"] == 1


@pytest.mark.asyncio
async def test_simple_loader_differs_calls_by_kwargs(user, other_user):
    context = {}
    assert await load_items(context)
    assert context
    assert await load_items(context, page=2)
    assert await load_items(context, page=2)
    assert context["hits"] == 2


@pytest.mark.asyncio
async def test_simple_loader_doesnt_lock_in_gather(user, other_user):
    context = {}
    assert await gather(
        load_items(context),
        load_items(context, page=2),
        load_items(context, page=2),
    )
    assert context
    assert context["hits"] == 2
