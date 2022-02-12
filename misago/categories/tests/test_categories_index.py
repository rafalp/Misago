import pytest

from ..index import get_categories_index


@pytest.mark.asyncio
async def test_getting_categories_index_returns_index_of_categories(category):
    categories = await get_categories_index()
    assert categories[category.id].id == category.id


@pytest.mark.asyncio
async def test_categories_index_returns_list_all_categories_ids(category):
    categories = await get_categories_index()
    assert category.id in categories.all_ids


@pytest.mark.asyncio
async def test_categories_index_returns_list_of_child_categories_ids(
    category, child_category
):
    categories = await get_categories_index()
    assert categories.get_children_ids(child_category.parent_id) == [child_category.id]


@pytest.mark.asyncio
async def test_categories_index_returns_list_of_child_categories_with_parents_ids(
    category, child_category
):
    categories = await get_categories_index()
    assert categories.get_children_ids(
        child_category.parent_id, include_parent=True
    ) == [child_category.parent_id, child_category.id]
