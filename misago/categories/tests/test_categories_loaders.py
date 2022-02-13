import pytest

from ..loaders import categories_children_loader, categories_loader


@pytest.mark.asyncio
async def test_categories_loader_loads_category(graphql_context, category):
    loaded_category = await categories_loader.load(graphql_context, category.id)
    assert loaded_category == category


@pytest.mark.asyncio
async def test_categories_children_loader_loads_child_categories(
    graphql_context, child_category
):
    child_categories = await categories_children_loader.load(
        graphql_context, child_category.parent_id
    )
    assert child_categories == [child_category]


@pytest.mark.asyncio
async def test_categories_children_loader_empty_list_for_leaf_nodes(
    graphql_context, sibling_category
):
    child_categories = await categories_children_loader.load(
        graphql_context, sibling_category.id
    )
    assert child_categories == []
