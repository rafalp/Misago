import pytest

from ..categories import load_categories, load_category, load_category_children


@pytest.mark.asyncio
async def test_top_level_categories_can_be_loaded(
    category, child_category, sibling_category
):
    loaded_categories = await load_categories({})
    assert category in loaded_categories
    assert child_category not in loaded_categories
    assert sibling_category in loaded_categories


@pytest.mark.asyncio
async def test_category_loader_returns_category(category):
    loaded_category = await load_category({}, category.id)
    assert loaded_category == category


@pytest.mark.asyncio
async def test_category_loader_returns_none_for_nonexistent_category_id(db):
    loaded_category = await load_category({}, 100)
    assert loaded_category is None


@pytest.mark.asyncio
async def test_category_child_loader_returns_category_children(
    category, child_category
):
    loaded_categories = await load_category_children({}, category.id)
    assert loaded_categories == [child_category]


@pytest.mark.asyncio
async def test_category_child_loader_returns_empty_list_for_nonexistant_category(db):
    loaded_categories = await load_category_children({}, 100)
    assert loaded_categories == []
