import pytest

from .....categories.get import get_category_by_id, get_categories_mptt
from ..createcategory import resolve_create_category


@pytest.mark.asyncio
async def test_create_category_mutation_creates_top_level_category(
    admin_graphql_info, categories
):
    data = await resolve_create_category(
        None, admin_graphql_info, input={"name": "New category"},
    )

    assert not data.get("errors")
    assert data["category"]

    new_category = await get_category_by_id(data["category"].id)
    assert new_category
    assert new_category.name == "New category"
    assert new_category.slug == "new-category"
    assert new_category.parent_id is None
    assert new_category.depth == 0
    assert new_category.left == 11
    assert new_category.right == 12
    assert not new_category.is_closed

    # Category is appended at the end of categories list
    db_categories = (await get_categories_mptt()).nodes()
    assert db_categories[-1] == new_category

    # Categories tree is valid
    categories_tree = [(i.depth, i.left, i.right) for i in db_categories]
    assert categories_tree == [
        (0, 1, 2),  # Example category
        (0, 3, 6),  # Category
        (1, 4, 5),  # - Child category
        (0, 7, 8),  # Sibling category
        (0, 9, 10),  # Closed category
        (0, 11, 12),  # New category
    ]


@pytest.mark.asyncio
async def test_create_category_mutation_creates_new_child_category(
    admin_graphql_info, categories, category
):
    data = await resolve_create_category(
        None,
        admin_graphql_info,
        input={"name": "New category", "parent": str(category.id)},
    )

    assert not data.get("errors")
    assert data["category"]

    new_category = await get_category_by_id(data["category"].id)
    assert new_category
    assert new_category.name == "New category"
    assert new_category.slug == "new-category"
    assert new_category.parent_id == category.id
    assert new_category.depth == 1
    assert new_category.left == 6
    assert new_category.right == 7

    # Category is appended to categories tree
    db_categories = (await get_categories_mptt()).nodes()
    assert db_categories[3] == new_category

    # Categories tree is valid
    categories_tree = [(i.depth, i.left, i.right) for i in db_categories]
    assert categories_tree == [
        (0, 1, 2),  # Example category
        (0, 3, 8),  # Category
        (1, 4, 5),  # - Child category
        (1, 6, 7),  # - New category
        (0, 9, 10),  # Sibling category
        (0, 11, 12),  # Closed category
    ]


@pytest.mark.asyncio
async def test_create_category_mutation_creates_closed_category(
    admin_graphql_info, categories
):
    data = await resolve_create_category(
        None, admin_graphql_info, input={"name": "New category", "isClosed": True},
    )

    assert not data.get("errors")
    assert data["category"]

    new_category = await get_category_by_id(data["category"].id)
    assert new_category
    assert new_category.depth == 0
    assert new_category.is_closed

    # Category is appended at the end of categories list
    db_categories = (await get_categories_mptt()).nodes()
    assert db_categories[-1] == new_category

    # Categories tree is valid
    categories_tree = [(i.depth, i.left, i.right) for i in db_categories]
    assert categories_tree == [
        (0, 1, 2),  # Example category
        (0, 3, 6),  # Category
        (1, 4, 5),  # - Child category
        (0, 7, 8),  # Sibling category
        (0, 9, 10),  # Closed category
        (0, 11, 12),  # New category
    ]
