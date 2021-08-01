import pytest

from .....categories.get import get_all_categories
from .....categories.models import Category

CATEGORY_CREATE_MUTATION = """
    mutation CategoryCreate($input: CategoryCreateInput!) {
        categoryCreate(input: $input) {
            errors {
                location
                type
            }
            category {
                id
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_category_create_mutation_creates_top_level_category(
    query_admin_api, categories
):
    variables = {"input": {"name": "New category"}}
    result = await query_admin_api(CATEGORY_CREATE_MUTATION, variables)
    data = result["data"]["categoryCreate"]
    assert not data["errors"]
    assert data["category"]

    new_category = await Category.query.one(id=int(data["category"]["id"]))
    assert new_category.name == "New category"
    assert new_category.slug == "new-category"
    assert new_category.color == "#0F0"
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
async def test_category_create_mutation_creates_new_child_category(
    query_admin_api, categories, category
):
    variables = {
        "input": {
            "name": "New category",
            "parent": str(category.id),
        }
    }
    result = await query_admin_api(CATEGORY_CREATE_MUTATION, variables)
    data = result["data"]["categoryCreate"]
    assert not data["errors"]
    assert data["category"]

    new_category = await Category.query.one(id=int(data["category"]["id"]))
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
async def test_category_create_mutation_creates_category_with_icon(
    query_admin_api, categories
):
    variables = {"input": {"name": "New category", "icon": "fas fa-lock"}}
    result = await query_admin_api(CATEGORY_CREATE_MUTATION, variables)
    data = result["data"]["categoryCreate"]
    assert not data["errors"]
    assert data["category"]

    new_category = await Category.query.one(id=int(data["category"]["id"]))
    assert new_category.icon == "fas fa-lock"


@pytest.mark.asyncio
async def test_category_create_mutation_creates_category_with_color(
    query_admin_api, categories
):
    variables = {"input": {"name": "New category", "color": "#99dd99"}}
    result = await query_admin_api(CATEGORY_CREATE_MUTATION, variables)
    data = result["data"]["categoryCreate"]
    assert not data["errors"]
    assert data["category"]

    new_category = await Category.query.one(id=int(data["category"]["id"]))
    assert new_category.color == "#9D9"


@pytest.mark.asyncio
async def test_category_create_mutation_fails_if_category_color_is_invalid(
    query_admin_api,
):
    variables = {"input": {"name": "New category", "color": "invalid"}}
    result = await query_admin_api(CATEGORY_CREATE_MUTATION, variables)
    data = result["data"]["categoryCreate"]
    assert not data["category"]
    assert data["errors"] == [{"location": ["color"], "type": "value_error.color"}]


@pytest.mark.asyncio
async def test_category_create_mutation_creates_closed_category(
    query_admin_api, categories
):
    variables = {"input": {"name": "New category", "isClosed": True}}
    result = await query_admin_api(CATEGORY_CREATE_MUTATION, variables)
    data = result["data"]["categoryCreate"]
    assert not data["errors"]
    assert data["category"]

    new_category = await Category.query.one(id=int(data["category"]["id"]))
    assert new_category.is_closed


@pytest.mark.asyncio
async def test_category_create_mutation_fails_if_category_name_is_too_short(
    query_admin_api,
):
    variables = {"input": {"name": "    "}}
    result = await query_admin_api(CATEGORY_CREATE_MUTATION, variables)
    data = result["data"]["categoryCreate"]
    assert not data["category"]
    assert data["errors"] == [
        {"location": ["name"], "type": "value_error.any_str.min_length"}
    ]


@pytest.mark.asyncio
async def test_category_create_mutation_fails_if_category_name_is_too_long(
    query_admin_api,
):
    variables = {"input": {"name": "a" * 256}}
    result = await query_admin_api(CATEGORY_CREATE_MUTATION, variables)
    data = result["data"]["categoryCreate"]
    assert not data["category"]
    assert data["errors"] == [
        {"location": ["name"], "type": "value_error.any_str.max_length"}
    ]


@pytest.mark.asyncio
async def test_category_create_mutation_fails_if_category_name_is_not_sluggable(
    query_admin_api,
):
    variables = {"input": {"name": "!!!!"}}
    result = await query_admin_api(CATEGORY_CREATE_MUTATION, variables)
    data = result["data"]["categoryCreate"]
    assert not data["category"]
    assert data["errors"] == [{"location": ["name"], "type": "value_error.str.regex"}]


@pytest.mark.asyncio
async def test_category_create_mutation_fails_if_parent_id_is_invalid(
    query_admin_api,
):
    variables = {"input": {"name": "New category", "parent": "invalid"}}
    result = await query_admin_api(CATEGORY_CREATE_MUTATION, variables)
    data = result["data"]["categoryCreate"]
    assert not data["category"]
    assert data["errors"] == [{"location": ["parent"], "type": "type_error.integer"}]


@pytest.mark.asyncio
async def test_category_create_mutation_fails_if_parent_category_is_not_found(
    query_admin_api,
):
    variables = {"input": {"name": "New category", "parent": "1"}}
    result = await query_admin_api(CATEGORY_CREATE_MUTATION, variables)
    data = result["data"]["categoryCreate"]
    assert not data["category"]
    assert data["errors"] == [
        {"location": ["parent"], "type": "value_error.category.not_exists"}
    ]


@pytest.mark.asyncio
async def test_category_create_mutation_fails_if_parent_category_is_child_category(
    query_admin_api, child_category
):
    variables = {"input": {"name": "New category", "parent": str(child_category.id)}}
    result = await query_admin_api(CATEGORY_CREATE_MUTATION, variables)
    data = result["data"]["categoryCreate"]
    assert not data["category"]
    assert data["errors"] == [
        {"location": ["parent"], "type": "value_error.category.invalid_parent"}
    ]


@pytest.mark.asyncio
async def test_category_create_mutation_requires_admin_auth(query_admin_api):
    variables = {"input": {"name": "New category"}}
    result = await query_admin_api(
        CATEGORY_CREATE_MUTATION, variables, include_auth=False, expect_error=True
    )
    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"] is None
