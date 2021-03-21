import pytest

from .....categories.get import get_all_categories, get_category_by_id
from ..movecategory import resolve_move_category


@pytest.mark.asyncio
async def test_move_category_mutation_moves_sibling_category_before_other_category(
    admin_graphql_info, category, sibling_category
):
    data = await resolve_move_category(
        None,
        admin_graphql_info,
        category=str(sibling_category.id),
        before=str(category.id),
    )

    assert not data.get("errors")
    assert data["category"]

    moved_category = await get_category_by_id(data["category"].id)
    assert moved_category.id == sibling_category.id
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
        (1, 6, 7),  # Child category
        (0, 9, 10),  # Closed category
    ]


@pytest.mark.asyncio
async def test_move_category_mutation_moves_sibling_category_before_child_category(
    admin_graphql_info, category, child_category, sibling_category
):
    data = await resolve_move_category(
        None,
        admin_graphql_info,
        category=str(sibling_category.id),
        parent=str(category.id),
        before=str(child_category.id),
    )

    assert not data.get("errors")
    assert data["category"]

    moved_category = await get_category_by_id(data["category"].id)
    assert moved_category.id == sibling_category.id
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
        (1, 4, 5),  # Sibling category
        (1, 6, 7),  # Child category
        (0, 9, 10),  # Closed category
    ]


@pytest.mark.asyncio
async def test_move_category_mutation_moves_sibling_category_after_child_category(
    admin_graphql_info, category, sibling_category
):
    data = await resolve_move_category(
        None,
        admin_graphql_info,
        category=str(sibling_category.id),
        parent=str(category.id),
    )

    assert not data.get("errors")
    assert data["category"]

    moved_category = await get_category_by_id(data["category"].id)
    assert moved_category.id == sibling_category.id
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
        (1, 4, 5),  # Child category
        (1, 6, 7),  # Sibling category
        (0, 9, 10),  # Closed category
    ]


@pytest.mark.asyncio
async def test_move_category_mutation_moves_child_category_to_root(
    admin_graphql_info, child_category
):
    data = await resolve_move_category(
        None,
        admin_graphql_info,
        category=str(child_category.id),
    )

    assert not data.get("errors")
    assert data["category"]

    moved_category = await get_category_by_id(data["category"].id)
    assert moved_category.id == child_category.id
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
async def test_move_category_mutation_moves_child_category_to_root_before_parent(
    admin_graphql_info, category, child_category
):
    data = await resolve_move_category(
        None,
        admin_graphql_info,
        category=str(child_category.id),
        before=str(category.id),
    )

    assert not data.get("errors")
    assert data["category"]

    moved_category = await get_category_by_id(data["category"].id)
    assert moved_category.id == child_category.id
    assert moved_category.parent_id is None
    assert moved_category.depth == 0
    assert moved_category.left == 3
    assert moved_category.right == 4

    # Categories tree is valid
    db_categories = await get_all_categories()
    categories_tree = [(i.depth, i.left, i.right) for i in db_categories]
    assert categories_tree == [
        (0, 1, 2),  # Example category
        (0, 3, 4),  # Child category
        (0, 5, 6),  # Category
        (0, 7, 8),  # Sibling category
        (0, 9, 10),  # Closed category
    ]


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_category_id_is_invalid(
    admin_graphql_info, category
):
    data = await resolve_move_category(
        None,
        admin_graphql_info,
        category="invalid",
    )

    assert not data.get("category")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["category"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_parent_id_is_invalid(
    admin_graphql_info, category
):
    data = await resolve_move_category(
        None,
        admin_graphql_info,
        category=str(category.id),
        parent="invalid",
    )

    assert data.get("category")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["parent"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_before_id_is_invalid(
    admin_graphql_info, category
):
    data = await resolve_move_category(
        None,
        admin_graphql_info,
        category=str(category.id),
        before="invalid",
    )

    assert data.get("category")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["before"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_category_id_doesnt_exist(
    admin_graphql_info, category
):
    data = await resolve_move_category(
        None,
        admin_graphql_info,
        category=str(category.id + 1000),
    )

    assert not data.get("category")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["category"]
    assert data["errors"].get_errors_types() == ["value_error.category.not_exists"]


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_parent_id_doesnt_exist(
    admin_graphql_info, category
):
    data = await resolve_move_category(
        None,
        admin_graphql_info,
        category=str(category.id),
        parent=str(category.id + 1000),
    )

    assert data.get("category")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["parent"]
    assert data["errors"].get_errors_types() == ["value_error.category.not_exists"]


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_category_parent_is_itself(
    admin_graphql_info, category
):
    data = await resolve_move_category(
        None,
        admin_graphql_info,
        category=str(category.id),
        parent=str(category.id),
    )

    assert data.get("category")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["parent"]
    assert data["errors"].get_errors_types() == ["value_error.category.invalid_parent"]


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_category_before_is_itself(
    admin_graphql_info, category
):
    data = await resolve_move_category(
        None,
        admin_graphql_info,
        category=str(category.id),
        before=str(category.id),
    )

    assert data.get("category")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["before"]
    assert data["errors"].get_errors_types() == ["value_error.category.invalid_parent"]


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_parent_is_child_category(
    admin_graphql_info, category, child_category
):
    data = await resolve_move_category(
        None,
        admin_graphql_info,
        category=str(category.id),
        parent=str(child_category.id),
    )

    assert data.get("category")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["parent"]
    assert data["errors"].get_errors_types() == ["value_error.category.invalid_parent"]


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_root_category_is_moved_after_child(
    admin_graphql_info, category, child_category
):
    data = await resolve_move_category(
        None,
        admin_graphql_info,
        category=str(category.id),
        before=str(child_category.id),
    )

    assert data.get("category")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["before"]
    assert data["errors"].get_errors_types() == ["value_error.category.invalid_parent"]


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_child_is_moved_after_root(
    admin_graphql_info, category, child_category, sibling_category
):
    data = await resolve_move_category(
        None,
        admin_graphql_info,
        category=str(child_category.id),
        parent=str(category.id),
        before=str(sibling_category.id),
    )

    assert data.get("category")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["before"]
    assert data["errors"].get_errors_types() == ["value_error.category.invalid_parent"]
