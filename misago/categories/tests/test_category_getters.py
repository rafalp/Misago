import pytest

from ..get import get_all_categories, get_category_by_id, get_root_categories


@pytest.mark.asyncio
async def test_all_categories_list_can_be_get(category, child_category):
    categories = await get_all_categories()
    assert category in categories
    assert child_category in categories


@pytest.mark.asyncio
async def test_rot_categories_list_can_be_get(category, child_category):
    categories = await get_root_categories()
    assert category in categories
    assert child_category not in categories


@pytest.mark.asyncio
async def test_category_can_be_get_by_id(category):
    assert category == await get_category_by_id(category.id)


@pytest.mark.asyncio
async def test_getting_category_by_nonexistant_id_returns_none(db):
    assert await get_category_by_id(2000) is None
