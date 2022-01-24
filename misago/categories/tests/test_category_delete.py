import pytest

from .. import tree
from ..get import get_all_categories


@pytest.mark.asyncio
async def test_category_is_deleted_from_tree(sibling_category):
    categories = await tree.delete_category(
        await get_all_categories(), sibling_category
    )

    db_categories = await get_all_categories()
    assert sibling_category not in db_categories
    assert db_categories == categories

    # Categories tree is valid
    categories_tree = [(i.depth, i.left, i.right) for i in db_categories]
    assert categories_tree == [
        (0, 1, 2),  # Example category
        (0, 3, 6),  # Category
        (1, 4, 5),  # - Child category
        (0, 7, 8),  # Closed category
    ]


@pytest.mark.asyncio
async def test_category_and_its_children_are_deleted_from_tree(
    category, child_category
):
    categories = await tree.delete_category(await get_all_categories(), category)

    db_categories = await get_all_categories()
    assert category not in db_categories
    assert child_category not in db_categories
    assert db_categories == categories

    # Categories tree is valid
    categories_tree = [(i.depth, i.left, i.right) for i in db_categories]
    assert categories_tree == [
        (0, 1, 2),  # Example category
        (0, 3, 4),  # Sibling category
        (0, 5, 6),  # Closed category
    ]
