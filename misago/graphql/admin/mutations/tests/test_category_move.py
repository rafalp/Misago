import pytest

from .....categories.get import get_all_categories
from .....categories.models import Category

CATEGORY_MOVE_MUTATION = """
    mutation CategoryMove(
        $category: ID!, $parent: ID, $before: ID
    ) {
        categoryMove(
            category: $category,
            parent: $parent,
            before: $before
        ) {
            errors {
                location
                type
            }
            category {
                id
            }
            categories {
                id
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_move_category_mutation_moves_sibling_category_before_other_category(
    query_admin_api, category, sibling_category
):
    variables = {"category": str(sibling_category.id), "before": str(category.id)}
    result = await query_admin_api(CATEGORY_MOVE_MUTATION, variables)
    data = result["data"]["categoryMove"]
    assert not data["errors"]
    assert data["category"]
    assert data["categories"][0]["id"]

    moved_category = await Category.query.one(id=int(data["category"]["id"]))
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
    query_admin_api, category, child_category, sibling_category
):
    variables = {
        "category": str(sibling_category.id),
        "parent": str(category.id),
        "before": str(child_category.id),
    }
    result = await query_admin_api(CATEGORY_MOVE_MUTATION, variables)
    data = result["data"]["categoryMove"]
    assert not data["errors"]
    assert data["category"]
    assert data["categories"][0]["id"]

    moved_category = await Category.query.one(id=int(data["category"]["id"]))
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
    query_admin_api, category, sibling_category
):
    variables = {
        "category": str(sibling_category.id),
        "parent": str(category.id),
    }
    result = await query_admin_api(CATEGORY_MOVE_MUTATION, variables)
    data = result["data"]["categoryMove"]
    assert not data["errors"]
    assert data["category"]
    assert data["categories"][0]["id"]

    moved_category = await Category.query.one(id=int(data["category"]["id"]))
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
    query_admin_api, child_category
):
    variables = {
        "category": str(child_category.id),
    }
    result = await query_admin_api(CATEGORY_MOVE_MUTATION, variables)
    data = result["data"]["categoryMove"]
    assert not data["errors"]
    assert data["category"]
    assert data["categories"][0]["id"]

    moved_category = await Category.query.one(id=int(data["category"]["id"]))
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
    query_admin_api, category, child_category
):
    variables = {
        "category": str(child_category.id),
        "before": str(category.id),
    }
    result = await query_admin_api(CATEGORY_MOVE_MUTATION, variables)
    data = result["data"]["categoryMove"]
    assert not data["errors"]
    assert data["category"]
    assert data["categories"][0]["id"]

    moved_category = await Category.query.one(id=int(data["category"]["id"]))
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
    query_admin_api, category
):
    variables = {
        "category": "invalid",
    }
    result = await query_admin_api(CATEGORY_MOVE_MUTATION, variables)
    data = result["data"]["categoryMove"]
    assert not data["category"]
    assert data["categories"][0]["id"]
    assert data["errors"] == [{"location": ["category"], "type": "type_error.integer"}]


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_parent_id_is_invalid(
    query_admin_api, category
):
    variables = {
        "category": str(category.id),
        "parent": "invalid",
    }
    result = await query_admin_api(CATEGORY_MOVE_MUTATION, variables)
    data = result["data"]["categoryMove"]
    assert data["category"]
    assert data["categories"][0]["id"]
    assert data["errors"] == [{"location": ["parent"], "type": "type_error.integer"}]


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_before_id_is_invalid(
    query_admin_api, category
):
    variables = {
        "category": str(category.id),
        "before": "invalid",
    }
    result = await query_admin_api(CATEGORY_MOVE_MUTATION, variables)
    data = result["data"]["categoryMove"]
    assert data["category"]
    assert data["categories"][0]["id"]
    assert data["errors"] == [{"location": ["before"], "type": "type_error.integer"}]


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_category_id_doesnt_exist(
    query_admin_api, category
):
    variables = {
        "category": str(category.id + 1000),
    }
    result = await query_admin_api(CATEGORY_MOVE_MUTATION, variables)
    data = result["data"]["categoryMove"]
    assert not data["category"]
    assert data["categories"][0]["id"]
    assert data["errors"] == [
        {"location": ["category"], "type": "value_error.category.not_exists"}
    ]


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_parent_id_doesnt_exist(
    query_admin_api, category
):
    variables = {
        "category": str(category.id),
        "parent": str(category.id + 1000),
    }
    result = await query_admin_api(CATEGORY_MOVE_MUTATION, variables)
    data = result["data"]["categoryMove"]
    assert data["category"]
    assert data["categories"][0]["id"]
    assert data["errors"] == [
        {"location": ["parent"], "type": "value_error.category.not_exists"}
    ]


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_before_id_doesnt_exist(
    query_admin_api, category
):
    variables = {
        "category": str(category.id),
        "before": str(category.id + 1000),
    }
    result = await query_admin_api(CATEGORY_MOVE_MUTATION, variables)
    data = result["data"]["categoryMove"]
    assert data["category"]
    assert data["categories"][0]["id"]
    assert data["errors"] == [
        {"location": ["before"], "type": "value_error.category.not_exists"}
    ]


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_category_parent_is_itself(
    query_admin_api, category
):
    variables = {
        "category": str(category.id),
        "parent": str(category.id),
    }
    result = await query_admin_api(CATEGORY_MOVE_MUTATION, variables)
    data = result["data"]["categoryMove"]
    assert data["category"]
    assert data["categories"][0]["id"]
    assert data["errors"] == [
        {"location": ["parent"], "type": "value_error.category.invalid_parent"}
    ]


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_category_before_is_itself(
    query_admin_api, category
):
    variables = {
        "category": str(category.id),
        "before": str(category.id),
    }
    result = await query_admin_api(CATEGORY_MOVE_MUTATION, variables)
    data = result["data"]["categoryMove"]
    assert data["category"]
    assert data["categories"][0]["id"]
    assert data["errors"] == [
        {"location": ["before"], "type": "value_error.category.invalid_parent"}
    ]


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_parent_is_child_category(
    query_admin_api, category, child_category
):
    variables = {
        "category": str(category.id),
        "parent": str(child_category.id),
    }
    result = await query_admin_api(CATEGORY_MOVE_MUTATION, variables)
    data = result["data"]["categoryMove"]
    assert data["category"]
    assert data["categories"][0]["id"]
    assert data["errors"] == [
        {"location": ["parent"], "type": "value_error.category.invalid_parent"}
    ]


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_root_category_is_moved_after_child(
    query_admin_api, category, child_category
):
    variables = {
        "category": str(category.id),
        "before": str(child_category.id),
    }
    result = await query_admin_api(CATEGORY_MOVE_MUTATION, variables)
    data = result["data"]["categoryMove"]
    assert data["category"]
    assert data["categories"][0]["id"]
    assert data["errors"] == [
        {"location": ["before"], "type": "value_error.category.invalid_parent"}
    ]


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_child_is_moved_after_root(
    query_admin_api, category, child_category, sibling_category
):
    variables = {
        "category": str(child_category.id),
        "parent": str(category.id),
        "before": str(sibling_category.id),
    }
    result = await query_admin_api(CATEGORY_MOVE_MUTATION, variables)
    data = result["data"]["categoryMove"]
    assert data["category"]
    assert data["categories"][0]["id"]
    assert data["errors"] == [
        {"location": ["before"], "type": "value_error.category.invalid_parent"}
    ]


@pytest.mark.asyncio
async def test_category_move_mutation_requires_admin_auth(query_admin_api, category):
    variables = {
        "category": str(category.id),
    }
    result = await query_admin_api(
        CATEGORY_MOVE_MUTATION, variables, include_auth=False, expect_error=True
    )
    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"] is None
