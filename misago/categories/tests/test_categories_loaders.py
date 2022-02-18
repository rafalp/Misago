import pytest

from ..loaders import categories_children_loader, categories_loader


@pytest.mark.asyncio
async def test_categories_loader_loads_category(category, context):
    loaded_category = await categories_loader.load(context, category.id)
    assert loaded_category == category


@pytest.mark.asyncio
async def test_categories_children_loader_loads_child_categories(
    child_category, context
):
    child_categories = await categories_children_loader.load(
        context, child_category.parent_id
    )
    assert child_categories == [child_category]


@pytest.mark.asyncio
async def test_categories_children_loader_empty_list_for_leaf_nodes(
    sibling_category, context
):
    child_categories = await categories_children_loader.load(
        context, sibling_category.id
    )
    assert child_categories == []
