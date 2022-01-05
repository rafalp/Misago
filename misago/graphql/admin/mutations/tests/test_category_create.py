from unittest.mock import ANY

import pytest

from .....categories.get import get_all_categories
from .....categories.models import Category

CATEGORY_CREATE_MUTATION = """
    mutation CategoryCreate($input: CategoryCreateInput!) {
        categoryCreate(input: $input) {
            category {
                id
                name
                icon
                color
                parent {
                    id
                }
                isClosed
            }
            errors {
                location
                type
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_category_create_mutation_creates_top_level_category(
    query_admin_api, categories
):
    result = await query_admin_api(
        CATEGORY_CREATE_MUTATION,
        {
            "input": {
                "name": "New category",
            },
        },
    )

    data = result["data"]["categoryCreate"]

    assert data == {
        "category": {
            "id": ANY,
            "name": "New category",
            "icon": None,
            "color": "#0F0",
            "parent": None,
            "isClosed": False,
        },
        "errors": None,
    }

    category_from_db = await Category.query.one(id=int(data["category"]["id"]))
    assert category_from_db.name == "New category"
    assert category_from_db.slug == "new-category"
    assert category_from_db.color == "#0F0"
    assert category_from_db.icon is None
    assert category_from_db.parent_id is None
    assert category_from_db.depth == 0
    assert category_from_db.left == 11
    assert category_from_db.right == 12
    assert not category_from_db.is_closed

    # Category is appended at the end of categories list
    db_categories = await get_all_categories()
    assert db_categories[-1] == category_from_db

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
    result = await query_admin_api(
        CATEGORY_CREATE_MUTATION,
        {
            "input": {
                "name": "New category",
                "parent": str(category.id),
            },
        },
    )

    data = result["data"]["categoryCreate"]

    assert data == {
        "category": {
            "id": ANY,
            "name": "New category",
            "icon": None,
            "color": "#0F0",
            "parent": {
                "id": str(category.id),
            },
            "isClosed": False,
        },
        "errors": None,
    }

    category_from_db = await Category.query.one(id=int(data["category"]["id"]))
    assert category_from_db.parent_id == category.id
    assert category_from_db.depth == 1
    assert category_from_db.left == 6
    assert category_from_db.right == 7

    # Category is appended to categories tree
    db_categories = await get_all_categories()
    assert db_categories[3] == category_from_db

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
    result = await query_admin_api(
        CATEGORY_CREATE_MUTATION,
        {
            "input": {
                "name": "New category",
                "icon": "fas fa-lock",
            },
        },
    )

    data = result["data"]["categoryCreate"]

    assert data == {
        "category": {
            "id": ANY,
            "name": "New category",
            "icon": "fas fa-lock",
            "color": "#0F0",
            "parent": None,
            "isClosed": False,
        },
        "errors": None,
    }

    category_from_db = await Category.query.one(id=int(data["category"]["id"]))
    assert category_from_db.icon == "fas fa-lock"


@pytest.mark.asyncio
async def test_category_create_mutation_creates_category_with_color(
    query_admin_api, categories
):
    result = await query_admin_api(
        CATEGORY_CREATE_MUTATION,
        {
            "input": {
                "name": "New category",
                "color": "#99dd99",
            },
        },
    )

    data = result["data"]["categoryCreate"]

    assert data == {
        "category": {
            "id": ANY,
            "name": "New category",
            "icon": None,
            "color": "#9D9",
            "parent": None,
            "isClosed": False,
        },
        "errors": None,
    }

    category_from_db = await Category.query.one(id=int(data["category"]["id"]))
    assert category_from_db.color == "#9D9"


@pytest.mark.asyncio
async def test_category_create_mutation_fails_if_category_color_is_invalid(
    query_admin_api,
):
    result = await query_admin_api(
        CATEGORY_CREATE_MUTATION,
        {
            "input": {
                "name": "New category",
                "color": "invalid",
            },
        },
    )

    assert result["data"]["categoryCreate"] == {
        "category": None,
        "errors": [
            {
                "location": ["color"],
                "type": "value_error.color",
            },
        ],
    }


@pytest.mark.asyncio
async def test_category_create_mutation_creates_closed_category(
    query_admin_api, categories
):
    result = await query_admin_api(
        CATEGORY_CREATE_MUTATION,
        {
            "input": {
                "name": "New category",
                "isClosed": True,
            },
        },
    )

    data = result["data"]["categoryCreate"]

    assert data == {
        "category": {
            "id": ANY,
            "name": "New category",
            "icon": None,
            "color": "#0F0",
            "parent": None,
            "isClosed": True,
        },
        "errors": None,
    }

    category_from_db = await Category.query.one(id=int(data["category"]["id"]))
    assert category_from_db.is_closed


@pytest.mark.asyncio
async def test_category_create_mutation_fails_if_category_name_is_too_short(
    query_admin_api,
):
    result = await query_admin_api(
        CATEGORY_CREATE_MUTATION,
        {
            "input": {
                "name": "   ",
            },
        },
    )

    assert result["data"]["categoryCreate"] == {
        "category": None,
        "errors": [
            {
                "location": ["name"],
                "type": "value_error.any_str.min_length",
            }
        ],
    }


@pytest.mark.asyncio
async def test_category_create_mutation_fails_if_category_name_is_too_long(
    query_admin_api,
):
    result = await query_admin_api(
        CATEGORY_CREATE_MUTATION,
        {
            "input": {
                "name": "A" * 256,
            },
        },
    )

    assert result["data"]["categoryCreate"] == {
        "category": None,
        "errors": [
            {
                "location": ["name"],
                "type": "value_error.any_str.max_length",
            }
        ],
    }


@pytest.mark.asyncio
async def test_category_create_mutation_fails_if_category_name_is_not_sluggable(
    query_admin_api,
):
    result = await query_admin_api(
        CATEGORY_CREATE_MUTATION,
        {
            "input": {
                "name": "!@#$",
            },
        },
    )

    assert result["data"]["categoryCreate"] == {
        "category": None,
        "errors": [
            {
                "location": ["name"],
                "type": "value_error.str.regex",
            }
        ],
    }


@pytest.mark.asyncio
async def test_category_create_mutation_fails_if_parent_id_is_invalid(
    query_admin_api,
):
    result = await query_admin_api(
        CATEGORY_CREATE_MUTATION,
        {
            "input": {
                "name": "New category",
                "parent": "invalid",
            },
        },
    )

    assert result["data"]["categoryCreate"] == {
        "category": None,
        "errors": [
            {
                "location": ["parent"],
                "type": "type_error.integer",
            }
        ],
    }


@pytest.mark.asyncio
async def test_category_create_mutation_fails_if_parent_category_is_not_found(
    query_admin_api,
):
    result = await query_admin_api(
        CATEGORY_CREATE_MUTATION,
        {
            "input": {
                "name": "New category",
                "parent": "1",
            },
        },
    )

    assert result["data"]["categoryCreate"] == {
        "category": None,
        "errors": [
            {
                "location": ["parent"],
                "type": "value_error.category.not_exists",
            }
        ],
    }


@pytest.mark.asyncio
async def test_category_create_mutation_fails_if_parent_category_is_child_category(
    query_admin_api, child_category
):
    result = await query_admin_api(
        CATEGORY_CREATE_MUTATION,
        {
            "input": {
                "name": "New category",
                "parent": str(child_category.id),
            },
        },
    )

    assert result["data"]["categoryCreate"] == {
        "category": None,
        "errors": [
            {
                "location": ["parent"],
                "type": "value_error.category.invalid_parent",
            }
        ],
    }


@pytest.mark.asyncio
async def test_category_create_mutation_requires_admin_auth(query_admin_api):
    result = await query_admin_api(
        CATEGORY_CREATE_MUTATION,
        {
            "input": {
                "name": "New category",
            },
        },
        include_auth=False,
        expect_error=True,
    )

    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"] is None
