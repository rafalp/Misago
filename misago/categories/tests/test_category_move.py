import pytest

from ..get import get_all_categories
from ..tree import CategoryTreeUpdateError, move_category


@pytest.mark.asyncio
async def test_sibling_category_is_moved_under_category_at_the_end(
    admin_graphql_info, category, sibling_category
):
    all_categories = await get_all_categories()
    moved_category = await move_category(
        all_categories, sibling_category, parent=category
    )

    # Category contents are updated
    assert moved_category.parent_id == category.id
    assert moved_category.depth == 1
    assert moved_category.left == 6
    assert moved_category.right == 7

    # Categories tree is valid
    db_categories = await get_all_categories()
    categories_tree = [(i.depth, i.left, i.right) for i in db_categories]
    assert categories_tree == [
        (0, 1, 2),  # Example category
        (0, 3, 8),  # Category
        (1, 4, 5),  # - Child category
        (1, 6, 7),  # - Sibling category
        (0, 9, 10),  # Closed category
    ]


@pytest.mark.asyncio
async def test_sibling_category_is_moved_under_category_before_child(
    admin_graphql_info, category, child_category, sibling_category
):
    all_categories = await get_all_categories()
    moved_category = await move_category(
        all_categories, sibling_category, parent=category, before=child_category
    )

    # Category contents are updated
    assert moved_category.parent_id == category.id
    assert moved_category.depth == 1
    assert moved_category.left == 4
    assert moved_category.right == 5

    # Categories tree is valid
    db_categories = await get_all_categories()
    categories_tree = [(i.depth, i.left, i.right) for i in db_categories]
    assert categories_tree == [
        (0, 1, 2),  # Example category
        (0, 3, 8),  # Category
        (1, 4, 5),  # - Sibling category
        (1, 6, 7),  # - Child category
        (0, 9, 10),  # Closed category
    ]


@pytest.mark.asyncio
async def test_sibling_category_is_moved_before_category(
    admin_graphql_info, category, sibling_category
):
    all_categories = await get_all_categories()
    moved_category = await move_category(
        all_categories, sibling_category, before=category
    )

    # Category contents are updated
    assert moved_category.parent_id is None
    assert moved_category.depth == 0
    assert moved_category.left == 3
    assert moved_category.right == 4

    # Categories tree is valid
    db_categories = await get_all_categories()
    categories_tree = [(i.depth, i.left, i.right) for i in db_categories]
    assert categories_tree == [
        (0, 1, 2),  # Example category
        (0, 3, 4),  # Sibling category
        (0, 5, 8),  # Category
        (1, 6, 7),  # - Child category
        (0, 9, 10),  # Closed category
    ]


@pytest.mark.asyncio
async def test_child_category_is_moved_to_root_at_the_end(
    admin_graphql_info, category, child_category
):
    all_categories = await get_all_categories()
    moved_category = await move_category(all_categories, child_category)

    # Category contents are updated
    assert moved_category.parent_id is None
    assert moved_category.depth == 0
    assert moved_category.left == 9
    assert moved_category.right == 10

    # Categories tree is valid
    db_categories = await get_all_categories()
    categories_tree = [(i.depth, i.left, i.right) for i in db_categories]
    assert categories_tree == [
        (0, 1, 2),  # Example category
        (0, 3, 4),  # Category
        (0, 5, 6),  # Sibling category
        (0, 7, 8),  # Closed category
        (0, 9, 10),  # Child category
    ]


@pytest.mark.asyncio
async def test_child_category_is_moved_to_root_before_closed_category(
    admin_graphql_info, category, child_category, closed_category
):
    all_categories = await get_all_categories()
    moved_category = await move_category(
        all_categories, child_category, before=closed_category
    )

    # Category contents are updated
    assert moved_category.parent_id is None
    assert moved_category.depth == 0
    assert moved_category.left == 7
    assert moved_category.right == 8

    # Categories tree is valid
    db_categories = await get_all_categories()
    categories_tree = [(i.depth, i.left, i.right) for i in db_categories]
    assert categories_tree == [
        (0, 1, 2),  # Example category
        (0, 3, 4),  # Category
        (0, 5, 6),  # Sibling category
        (0, 7, 8),  # Child category
        (0, 9, 10),  # Closed category
    ]


@pytest.mark.asyncio
async def test_moving_category_under_itself_raises_validation_error(
    admin_graphql_info, category
):
    all_categories = await get_all_categories()

    with pytest.raises(CategoryTreeUpdateError):
        await move_category(all_categories, category, parent=category)


@pytest.mark.asyncio
async def test_moving_category_under_its_child_raises_validation_error(
    admin_graphql_info, category, child_category
):
    all_categories = await get_all_categories()

    with pytest.raises(CategoryTreeUpdateError):
        await move_category(all_categories, category, parent=child_category)


@pytest.mark.asyncio
async def test_moving_child_before_other_branch_category_raises_validation_error(
    admin_graphql_info, category, child_category, closed_category
):
    all_categories = await get_all_categories()

    with pytest.raises(CategoryTreeUpdateError):
        await move_category(
            all_categories, child_category, parent=category, before=closed_category
        )


@pytest.mark.asyncio
async def test_moving_category_before_itself_raises_validation_error(
    admin_graphql_info, category
):
    all_categories = await get_all_categories()

    with pytest.raises(CategoryTreeUpdateError):
        await move_category(all_categories, category, before=category)
