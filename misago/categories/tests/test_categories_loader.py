import pytest

from ..loaders import categories_loader


@pytest.mark.asyncio
async def test_categories_loader_loads_category(graphql_context, category):
    loaded_category = await categories_loader.load(graphql_context, category.id)
    assert loaded_category == category
