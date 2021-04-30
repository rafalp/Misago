import pytest

from ..get import get_all_categories
from ..models import Category
from ..tree import insert_category


@pytest.mark.asyncio
async def test_new_top_level_category_is_inserted_at_the_end_of_tree(
    admin_graphql_info, categories
):
    all_categories = await get_all_categories()

    new_category = await Category.create(name="New category", extra={})
    inserted_category, categories = await insert_category(all_categories, new_category)

    # Category contents are updated
    assert inserted_category.parent_id is None
    assert inserted_category.depth == 0
    assert inserted_category.left == 11
    assert inserted_category.right == 12

    # Category is appended at the end of categories list
    db_categories = await get_all_categories()
    assert db_categories[-1] == inserted_category
    assert db_categories == categories

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
async def test_new_child_category_is_inserted_at_the_end_of_tree(
    admin_graphql_info, categories, category
):
    all_categories = await get_all_categories()

    new_category = await Category.create(name="New category", extra={})
    inserted_category, categories = await insert_category(
        all_categories, new_category, category
    )

    # Category contents are updated
    assert inserted_category.parent_id == category.id
    assert inserted_category.depth == 1
    assert inserted_category.left == 6
    assert inserted_category.right == 7

    # Category is appended to categories tree
    db_categories = await get_all_categories()
    assert db_categories[3] == inserted_category
    assert db_categories == categories

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
