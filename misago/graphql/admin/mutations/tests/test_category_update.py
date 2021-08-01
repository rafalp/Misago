import pytest

from .....categories.get import get_all_categories
from .....categories.models import Category

CATEGORY_UPDATE_MUTATION = """
    mutation CategoryUpdate($category: ID!, $input: CategoryUpdateInput!) {
        categoryUpdate(category: $category, input: $input) {
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
async def test_category_update_mutation_edits_category_name(query_admin_api, category):
    variables = {
        "category": str(category.id),
        "input": {"name": "Edited category"},
    }
    result = await query_admin_api(CATEGORY_UPDATE_MUTATION, variables)
    data = result["data"]["categoryUpdate"]
    assert not data["errors"]
    assert data["category"]

    updated_category = await Category.query.one(id=int(data["category"]["id"]))
    assert updated_category.id == category.id
    assert updated_category.name == "Edited category"
    assert updated_category.slug == "edited-category"


@pytest.mark.asyncio
async def test_category_update_mutation_edits_category_color(query_admin_api, category):
    variables = {
        "category": str(category.id),
        "input": {"color": "#F0F0F0"},
    }
    result = await query_admin_api(CATEGORY_UPDATE_MUTATION, variables)
    data = result["data"]["categoryUpdate"]
    assert not data["errors"]
    assert data["category"]

    updated_category = await Category.query.one(id=int(data["category"]["id"]))
    assert updated_category.id == category.id
    assert updated_category.color == "#F0F0F0"


@pytest.mark.asyncio
async def test_category_update_mutation_edits_category_icon(query_admin_api, category):
    variables = {
        "category": str(category.id),
        "input": {"icon": "fas fa-lock"},
    }
    result = await query_admin_api(CATEGORY_UPDATE_MUTATION, variables)
    data = result["data"]["categoryUpdate"]
    assert not data["errors"]
    assert data["category"]

    updated_category = await Category.query.one(id=int(data["category"]["id"]))
    assert updated_category.id == category.id
    assert updated_category.icon == "fas fa-lock"


@pytest.mark.asyncio
async def test_category_update_mutation_removes_category_icon(
    query_admin_api, category
):
    await category.update(icon="fas fa-lock")

    variables = {
        "category": str(category.id),
        "input": {"icon": ""},
    }
    result = await query_admin_api(CATEGORY_UPDATE_MUTATION, variables)
    data = result["data"]["categoryUpdate"]
    assert not data["errors"]
    assert data["category"]

    updated_category = await Category.query.one(id=int(data["category"]["id"]))
    assert updated_category.id == category.id
    assert updated_category.icon is None


@pytest.mark.asyncio
async def test_category_update_mutation_closes_category(query_admin_api, category):
    variables = {
        "category": str(category.id),
        "input": {"isClosed": True},
    }
    result = await query_admin_api(CATEGORY_UPDATE_MUTATION, variables)
    data = result["data"]["categoryUpdate"]
    assert not data["errors"]
    assert data["category"]

    updated_category = await Category.query.one(id=int(data["category"]["id"]))
    assert updated_category.id == category.id
    assert updated_category.is_closed


@pytest.mark.asyncio
async def test_category_update_mutation_opens_category(
    query_admin_api, closed_category
):
    variables = {
        "category": str(closed_category.id),
        "input": {"isClosed": False},
    }
    result = await query_admin_api(CATEGORY_UPDATE_MUTATION, variables)
    data = result["data"]["categoryUpdate"]
    assert not data["errors"]
    assert data["category"]

    updated_category = await Category.query.one(id=int(data["category"]["id"]))
    assert updated_category.id == closed_category.id
    assert not updated_category.is_closed


@pytest.mark.asyncio
async def test_category_update_mutation_changes_child_category_to_root_category(
    query_admin_api, child_category
):
    variables = {
        "category": str(child_category.id),
        "input": {"parent": None},
    }
    result = await query_admin_api(CATEGORY_UPDATE_MUTATION, variables)
    data = result["data"]["categoryUpdate"]
    assert not data["errors"]
    assert data["category"]

    updated_category = await Category.query.one(id=int(data["category"]["id"]))
    assert updated_category.id == child_category.id
    assert updated_category.parent_id is None
    assert updated_category.depth == 0
    assert updated_category.left == 9
    assert updated_category.right == 10

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
async def test_category_update_mutation_changes_root_category_to_child_category(
    query_admin_api, category, sibling_category
):
    variables = {
        "category": str(sibling_category.id),
        "input": {"parent": str(category.id)},
    }
    result = await query_admin_api(CATEGORY_UPDATE_MUTATION, variables)
    data = result["data"]["categoryUpdate"]
    assert not data["errors"]
    assert data["category"]

    updated_category = await Category.query.one(id=int(data["category"]["id"]))
    assert updated_category.id == sibling_category.id
    assert updated_category.parent_id == category.id
    assert updated_category.depth == 1
    assert updated_category.left == 6
    assert updated_category.right == 7

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
async def test_category_update_mutation_fails_if_category_doesnt_exist(
    query_admin_api, category
):
    variables = {
        "category": str(category.id + 100),
        "input": {"name": "Updated Category"},
    }
    result = await query_admin_api(CATEGORY_UPDATE_MUTATION, variables)
    data = result["data"]["categoryUpdate"]
    assert not data["category"]
    assert data["errors"] == [
        {"location": ["category"], "type": "value_error.category.not_exists"}
    ]


@pytest.mark.asyncio
async def test_category_update_mutation_fails_if_category_id_is_invalid(
    query_admin_api, category
):
    variables = {
        "category": "invalid",
        "input": {"name": "Updated Category"},
    }
    result = await query_admin_api(CATEGORY_UPDATE_MUTATION, variables)
    data = result["data"]["categoryUpdate"]
    assert not data["category"]
    assert data["errors"] == [{"location": ["category"], "type": "type_error.integer"}]


@pytest.mark.asyncio
async def test_category_update_mutation_fails_if_category_name_is_too_short(
    query_admin_api, category
):
    variables = {
        "category": str(category.id),
        "input": {"name": "    "},
    }
    result = await query_admin_api(CATEGORY_UPDATE_MUTATION, variables)
    data = result["data"]["categoryUpdate"]
    assert data["category"]
    assert data["errors"] == [
        {"location": ["name"], "type": "value_error.any_str.min_length"}
    ]


@pytest.mark.asyncio
async def test_category_update_mutation_fails_if_category_name_is_too_long(
    query_admin_api, category
):
    variables = {
        "category": str(category.id),
        "input": {"name": "a" * 256},
    }
    result = await query_admin_api(CATEGORY_UPDATE_MUTATION, variables)
    data = result["data"]["categoryUpdate"]
    assert data["category"]
    assert data["errors"] == [
        {"location": ["name"], "type": "value_error.any_str.max_length"}
    ]


@pytest.mark.asyncio
async def test_category_update_mutation_fails_if_category_name_is_not_sluggable(
    query_admin_api, category
):
    variables = {
        "category": str(category.id),
        "input": {"name": "!!!!"},
    }
    result = await query_admin_api(CATEGORY_UPDATE_MUTATION, variables)
    data = result["data"]["categoryUpdate"]
    assert data["category"]
    assert data["errors"] == [{"location": ["name"], "type": "value_error.str.regex"}]


@pytest.mark.asyncio
async def test_category_update_mutation_fails_if_category_parent_is_invalid(
    query_admin_api, sibling_category
):
    variables = {
        "category": str(sibling_category.id),
        "input": {"parent": "invalid"},
    }
    result = await query_admin_api(CATEGORY_UPDATE_MUTATION, variables)
    data = result["data"]["categoryUpdate"]
    assert data["category"]
    assert data["errors"] == [{"location": ["parent"], "type": "type_error.integer"}]


@pytest.mark.asyncio
async def test_category_update_mutation_fails_if_category_parent_doesnt_exist(
    query_admin_api, sibling_category
):
    variables = {
        "category": str(sibling_category.id),
        "input": {"parent": str(sibling_category.id + 100)},
    }
    result = await query_admin_api(CATEGORY_UPDATE_MUTATION, variables)
    data = result["data"]["categoryUpdate"]
    assert data["category"]
    assert data["errors"] == [
        {"location": ["parent"], "type": "value_error.category.not_exists"}
    ]


@pytest.mark.asyncio
async def test_category_update_mutation_fails_if_category_parent_is_category(
    query_admin_api, sibling_category
):
    variables = {
        "category": str(sibling_category.id),
        "input": {"parent": str(sibling_category.id)},
    }
    result = await query_admin_api(CATEGORY_UPDATE_MUTATION, variables)
    data = result["data"]["categoryUpdate"]
    assert data["category"]
    assert data["errors"] == [
        {"location": ["parent"], "type": "value_error.category.invalid_parent"}
    ]


@pytest.mark.asyncio
async def test_category_update_mutation_fails_if_parent_is_child_category(
    query_admin_api, child_category, sibling_category
):
    variables = {
        "category": str(sibling_category.id),
        "input": {"parent": str(child_category.id)},
    }
    result = await query_admin_api(CATEGORY_UPDATE_MUTATION, variables)
    data = result["data"]["categoryUpdate"]
    assert data["category"]
    assert data["errors"] == [
        {"location": ["parent"], "type": "value_error.category.invalid_parent"}
    ]


@pytest.mark.asyncio
async def test_category_update_mutation_fails_if_category_has_children(
    query_admin_api, category, sibling_category
):
    variables = {
        "category": str(category.id),
        "input": {"parent": str(sibling_category.id)},
    }
    result = await query_admin_api(CATEGORY_UPDATE_MUTATION, variables)
    data = result["data"]["categoryUpdate"]
    assert data["category"]
    assert data["errors"] == [
        {"location": ["parent"], "type": "value_error.category.invalid_parent"}
    ]


@pytest.mark.asyncio
async def test_category_update_mutation_requires_admin_auth(query_admin_api, category):
    variables = {
        "category": str(category.id),
        "input": {"name": "Updated Category"},
    }
    result = await query_admin_api(
        CATEGORY_UPDATE_MUTATION, variables, include_auth=False, expect_error=True
    )
    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"] is None
