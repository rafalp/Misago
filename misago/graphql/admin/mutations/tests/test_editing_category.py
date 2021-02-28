import pytest

from .....categories.get import get_category_by_id, get_all_categories
from ..editcategory import resolve_edit_category


@pytest.mark.asyncio
async def test_edit_category_mutation_edits_category_name(admin_graphql_info, category):
    data = await resolve_edit_category(
        None,
        admin_graphql_info,
        category=str(category.id),
        input={"name": "Edited category"},
    )

    assert not data.get("errors")
    assert data["category"]

    edited_category = await get_category_by_id(data["category"].id)
    assert edited_category.id == category.id
    assert edited_category.name == "Edited category"
    assert edited_category.slug == "edited-category"


@pytest.mark.asyncio
async def test_edit_category_mutation_closes_category(admin_graphql_info, category):
    data = await resolve_edit_category(
        None,
        admin_graphql_info,
        category=str(category.id),
        input={"name": "Edited category", "isClosed": True},
    )

    assert not data.get("errors")
    assert data["category"]

    edited_category = await get_category_by_id(data["category"].id)
    assert edited_category.id == category.id
    assert edited_category.is_closed


@pytest.mark.asyncio
async def test_edit_category_mutation_opens_category(
    admin_graphql_info, closed_category
):
    data = await resolve_edit_category(
        None,
        admin_graphql_info,
        category=str(closed_category.id),
        input={"name": "Edited category", "isClosed": False},
    )

    assert not data.get("errors")
    assert data["category"]

    edited_category = await get_category_by_id(data["category"].id)
    assert edited_category.id == closed_category.id
    assert not edited_category.is_closed


@pytest.mark.asyncio
async def test_edit_category_mutation_changes_child_category_to_root_category(
    admin_graphql_info, child_category
):
    data = await resolve_edit_category(
        None,
        admin_graphql_info,
        category=str(child_category.id),
        input={"name": "Edited category"},
    )

    assert not data.get("errors")
    assert data["category"]

    edited_category = await get_category_by_id(data["category"].id)
    assert edited_category.id == child_category.id
    assert edited_category.parent_id is None
    assert edited_category.depth == 0
    assert edited_category.left == 9
    assert edited_category.right == 10

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
async def test_edit_category_mutation_changes_root_category_to_child_category(
    admin_graphql_info, category, sibling_category
):
    data = await resolve_edit_category(
        None,
        admin_graphql_info,
        category=str(sibling_category.id),
        input={"name": "Edited category", "parent": str(category.id)},
    )

    assert not data.get("errors")
    assert data["category"]

    edited_category = await get_category_by_id(data["category"].id)
    assert edited_category.id == sibling_category.id
    assert edited_category.parent_id == category.id
    assert edited_category.depth == 1
    assert edited_category.left == 6
    assert edited_category.right == 7

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
async def test_edit_category_mutation_fails_if_category_doesnt_exist(
    admin_graphql_info, category
):
    data = await resolve_edit_category(
        None,
        admin_graphql_info,
        category=str(category.id * 100),
        input={"name": "Category"},
    )

    assert not data.get("category")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["category"]
    assert data["errors"].get_errors_types() == ["value_error.category.not_exists"]


@pytest.mark.asyncio
async def test_edit_category_mutation_fails_if_category_id_is_invalid(
    admin_graphql_info, category
):
    data = await resolve_edit_category(
        None, admin_graphql_info, category="invalid", input={"name": "Category"},
    )

    assert not data.get("category")
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["category"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]


@pytest.mark.asyncio
async def test_edit_category_mutation_fails_if_category_name_is_too_short(
    admin_graphql_info, category
):
    data = await resolve_edit_category(
        None, admin_graphql_info, category=str(category.id), input={"name": "   "},
    )

    assert data.get("category")
    assert data["category"].name == "Category"
    assert data["category"].slug == "category"
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["name"]
    assert data["errors"].get_errors_types() == ["value_error.any_str.min_length"]


@pytest.mark.asyncio
async def test_edit_category_mutation_fails_if_category_name_is_too_long(
    admin_graphql_info, category
):
    data = await resolve_edit_category(
        None, admin_graphql_info, category=str(category.id), input={"name": "a" * 256},
    )

    assert data.get("category")
    assert data["category"].name == "Category"
    assert data["category"].slug == "category"
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["name"]
    assert data["errors"].get_errors_types() == ["value_error.any_str.max_length"]


@pytest.mark.asyncio
async def test_edit_category_mutation_fails_if_category_name_is_not_sluggable(
    admin_graphql_info, category
):
    data = await resolve_edit_category(
        None, admin_graphql_info, category=str(category.id), input={"name": "!!!!"},
    )

    assert data.get("category")
    assert data["category"].name == "Category"
    assert data["category"].slug == "category"
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["name"]
    assert data["errors"].get_errors_types() == ["value_error.str.regex"]


@pytest.mark.asyncio
async def test_edit_category_mutation_fails_if_category_parent_is_invalid(
    admin_graphql_info, sibling_category
):
    data = await resolve_edit_category(
        None,
        admin_graphql_info,
        category=str(sibling_category.id),
        input={"name": "Edited category", "parent": "invalid"},
    )

    assert data["category"]
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["parent"]
    assert data["errors"].get_errors_types() == ["type_error.integer"]


@pytest.mark.asyncio
async def test_edit_category_mutation_fails_if_category_parent_doesnt_exist(
    admin_graphql_info, sibling_category
):
    data = await resolve_edit_category(
        None,
        admin_graphql_info,
        category=str(sibling_category.id),
        input={"name": "Edited category", "parent": str(sibling_category.id * 100)},
    )

    assert data["category"]
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["parent"]
    assert data["errors"].get_errors_types() == ["value_error.category.not_exists"]


@pytest.mark.asyncio
async def test_edit_category_mutation_fails_if_category_parent_is_category(
    admin_graphql_info, sibling_category
):
    data = await resolve_edit_category(
        None,
        admin_graphql_info,
        category=str(sibling_category.id),
        input={"name": "Edited category", "parent": str(sibling_category.id)},
    )

    assert data["category"]
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["parent"]
    assert data["errors"].get_errors_types() == ["value_error.category.invalid_parent"]


@pytest.mark.asyncio
async def test_edit_category_mutation_fails_if_parent_is_child_category(
    admin_graphql_info, child_category, sibling_category
):
    data = await resolve_edit_category(
        None,
        admin_graphql_info,
        category=str(sibling_category.id),
        input={"name": "Edited category", "parent": str(child_category.id)},
    )

    assert data["category"]
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["parent"]
    assert data["errors"].get_errors_types() == ["value_error.category.invalid_parent"]


@pytest.mark.asyncio
async def test_edit_category_mutation_fails_if_category_has_children(
    admin_graphql_info, category, sibling_category
):
    data = await resolve_edit_category(
        None,
        admin_graphql_info,
        category=str(category.id),
        input={"name": "Edited category", "parent": str(sibling_category.id)},
    )

    assert data["category"]
    assert data.get("errors")
    assert data["errors"].get_errors_locations() == ["parent"]
    assert data["errors"].get_errors_types() == ["value_error.category.invalid_parent"]
