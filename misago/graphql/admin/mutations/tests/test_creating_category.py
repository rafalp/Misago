import pytest

from .....categories.get import get_all_categories, get_category_by_id
from ..createcategory import resolve_create_category


@pytest.mark.asyncio
async def test_create_category_mutation_creates_top_level_category(
    admin_graphql_info, categories
):
    data = await resolve_create_category(
        None,
        admin_graphql_info,
        input={"name": "New category", "color": "#FF0000", "icon": ""},
    )

    assert not data.get("errors")
    assert data["category"]

    new_category = await get_category_by_id(data["category"].id)
    assert new_category
    assert new_category.name == "New category"
    assert new_category.slug == "new-category"
    assert new_category.color == "#F00"
    assert new_category.icon is None
    assert new_category.parent_id is None
    assert new_category.depth == 0
    assert new_category.left == 11
    assert new_category.right == 12
    assert not new_category.is_closed

    # Category is appended at the end of categories list
    db_categories = await get_all_categories()
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
        input={
            "name": "New category",
            "color": "#FF0000",
            "icon": "",
            "parent": str(category.id),
        },
    )

    assert not data.get("errors")
    assert data["category"]

    new_category = await get_category_by_id(data["category"].id)
    assert new_category
    assert new_category.parent_id == category.id
    assert new_category.depth == 1
    assert new_category.left == 6
    assert new_category.right == 7

    # Category is appended to categories tree
    db_categories = await get_all_categories()
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
async def test_create_category_mutation_creates_category_with_icon(
    admin_graphql_info, categories
):
    data = await resolve_create_category(
        None,
        admin_graphql_info,
        input={"name": "New category", "color": "#FF0000", "icon": "fas fa-lock"},
    )

    assert not data.get("errors")
    assert data["category"]

    new_category = await get_category_by_id(data["category"].id)
    assert new_category
    assert new_category.icon == "fas fa-lock"


@pytest.mark.asyncio
async def test_create_category_mutation_creates_closed_category(
    admin_graphql_info, categories
):
    data = await resolve_create_category(
        None,
        admin_graphql_info,
        input={
            "name": "New category",
            "color": "#FF0000",
            "icon": "",
            "isClosed": True,
        },
    )

    assert not data.get("errors")
    assert data["category"]

    new_category = await get_category_by_id(data["category"].id)
    assert new_category
    assert new_category.is_closed


@pytest.mark.asyncio
async def test_create_category_mutation_fails_if_category_name_is_too_short(
    admin_graphql_info,
):
    data = await resolve_create_category(
        None,
        admin_graphql_info,
        input={"name": "   ", "color": "#FF0000", "icon": ""},
    )

    assert not data.get("category")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["name"]
    assert data["errors"].get_errors_types() == ["value_error.any_str.min_length"]


@pytest.mark.asyncio
async def test_create_category_mutation_fails_if_category_name_is_too_long(
    admin_graphql_info,
):
    data = await resolve_create_category(
        None,
        admin_graphql_info,
        input={"name": "a" * 256, "color": "#FF0000", "icon": ""},
    )

    assert not data.get("category")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["name"]
    assert data["errors"].get_errors_types() == ["value_error.any_str.max_length"]


@pytest.mark.asyncio
async def test_create_category_mutation_fails_if_category_name_is_not_sluggable(
    admin_graphql_info,
):
    data = await resolve_create_category(
        None,
        admin_graphql_info,
        input={"name": "!!!!", "color": "#FF0000", "icon": ""},
    )

    assert not data.get("category")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["name"]
    assert data["errors"].get_errors_types() == ["value_error.str.regex"]


@pytest.mark.asyncio
async def test_create_category_mutation_fails_if_category_color_is_empty(
    admin_graphql_info,
):
    data = await resolve_create_category(
        None,
        admin_graphql_info,
        input={"name": "Test", "color": "", "icon": ""},
    )

    assert not data.get("category")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["color"]
    assert data["errors"].get_errors_types() == ["value_error.color"]


@pytest.mark.asyncio
async def test_create_category_mutation_fails_if_category_color_is_invalid(
    admin_graphql_info,
):
    data = await resolve_create_category(
        None,
        admin_graphql_info,
        input={"name": "Test", "color": "invalid", "icon": ""},
    )

    assert not data.get("category")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["color"]
    assert data["errors"].get_errors_types() == ["value_error.color"]


@pytest.mark.asyncio
async def test_create_category_mutation_fails_if_parent_id_is_invalid(
    admin_graphql_info,
):
    data = await resolve_create_category(
        None,
        admin_graphql_info,
        input={
            "name": "New category",
            "color": "#FF0000",
            "icon": "",
            "parent": "invalid",
        },
    )

    assert not data.get("category")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["parent"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]


@pytest.mark.asyncio
async def test_create_category_mutation_fails_if_parent_category_is_not_found(
    admin_graphql_info,
):
    data = await resolve_create_category(
        None,
        admin_graphql_info,
        input={"name": "New category", "color": "#FF0000", "icon": "", "parent": 1},
    )

    assert not data.get("category")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["parent"]
    assert data["errors"].get_errors_types() == ["value_error.category.not_exists"]


@pytest.mark.asyncio
async def test_create_category_mutation_fails_if_parent_category_is_child_category(
    admin_graphql_info, child_category
):
    data = await resolve_create_category(
        None,
        admin_graphql_info,
        input={
            "name": "New category",
            "color": "#FF0000",
            "icon": "",
            "parent": str(child_category.id),
        },
    )

    assert not data.get("category")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["parent"]
    assert data["errors"].get_errors_types() == ["value_error.category.invalid_parent"]
