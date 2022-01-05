import pytest

from .....categories.get import get_all_categories
from .....categories.models import Category

CATEGORY_UPDATE_MUTATION = """
    mutation CategoryUpdate($category: ID!, $input: CategoryUpdateInput!) {
        categoryUpdate(category: $category, input: $input) {
            category {
                id
                name
                slug
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
async def test_category_update_mutation_edits_category_name(query_admin_api, category):
    result = await query_admin_api(
        CATEGORY_UPDATE_MUTATION,
        {
            "category": str(category.id),
            "input": {
                "name": "Edited category",
            },
        },
    )

    assert result["data"]["categoryUpdate"] == {
        "category": {
            "id": str(category.id),
            "name": "Edited category",
            "slug": "edited-category",
            "icon": None,
            "color": "#0F0",
            "parent": None,
            "isClosed": False,
        },
        "errors": None,
    }

    category_from_db = await category.refresh_from_db()
    assert category_from_db.name == "Edited category"
    assert category_from_db.slug == "edited-category"


@pytest.mark.asyncio
async def test_category_update_mutation_edits_category_color(query_admin_api, category):
    result = await query_admin_api(
        CATEGORY_UPDATE_MUTATION,
        {
            "category": str(category.id),
            "input": {
                "color": "#F0F0F0",
            },
        },
    )

    assert result["data"]["categoryUpdate"] == {
        "category": {
            "id": str(category.id),
            "name": "Category",
            "slug": "category",
            "icon": None,
            "color": "#F0F0F0",
            "parent": None,
            "isClosed": False,
        },
        "errors": None,
    }

    category_from_db = await category.refresh_from_db()
    assert category_from_db.id == category.id
    assert category_from_db.color == "#F0F0F0"


@pytest.mark.asyncio
async def test_category_update_mutation_edits_category_icon(query_admin_api, category):
    result = await query_admin_api(
        CATEGORY_UPDATE_MUTATION,
        {
            "category": str(category.id),
            "input": {
                "icon": "fas fa-lock",
            },
        },
    )

    assert result["data"]["categoryUpdate"] == {
        "category": {
            "id": str(category.id),
            "name": "Category",
            "slug": "category",
            "icon": "fas fa-lock",
            "color": "#0F0",
            "parent": None,
            "isClosed": False,
        },
        "errors": None,
    }

    category_from_db = await category.refresh_from_db()
    assert category_from_db.icon == "fas fa-lock"


@pytest.mark.asyncio
async def test_category_update_mutation_removes_category_icon(
    query_admin_api, category
):
    await category.update(icon="fas fa-lock")

    result = await query_admin_api(
        CATEGORY_UPDATE_MUTATION,
        {
            "category": str(category.id),
            "input": {
                "icon": "",
            },
        },
    )

    assert result["data"]["categoryUpdate"] == {
        "category": {
            "id": str(category.id),
            "name": "Category",
            "slug": "category",
            "icon": None,
            "color": "#0F0",
            "parent": None,
            "isClosed": False,
        },
        "errors": None,
    }

    category_from_db = await category.refresh_from_db()
    assert category_from_db.icon is None


@pytest.mark.asyncio
async def test_category_update_mutation_closes_category(query_admin_api, category):
    result = await query_admin_api(
        CATEGORY_UPDATE_MUTATION,
        {
            "category": str(category.id),
            "input": {
                "isClosed": True,
            },
        },
    )

    assert result["data"]["categoryUpdate"] == {
        "category": {
            "id": str(category.id),
            "name": "Category",
            "slug": "category",
            "icon": None,
            "color": "#0F0",
            "parent": None,
            "isClosed": True,
        },
        "errors": None,
    }

    category_from_db = await category.refresh_from_db()
    assert category_from_db.is_closed


@pytest.mark.asyncio
async def test_category_update_mutation_opens_category(
    query_admin_api, closed_category
):
    result = await query_admin_api(
        CATEGORY_UPDATE_MUTATION,
        {
            "category": str(closed_category.id),
            "input": {
                "isClosed": False,
            },
        },
    )

    assert result["data"]["categoryUpdate"] == {
        "category": {
            "id": str(closed_category.id),
            "name": "Closed Category",
            "slug": "closed-category",
            "icon": None,
            "color": "#0F0",
            "parent": None,
            "isClosed": False,
        },
        "errors": None,
    }

    category_from_db = await closed_category.refresh_from_db()
    assert not category_from_db.is_closed


@pytest.mark.asyncio
async def test_category_update_mutation_changes_child_category_to_root_category(
    query_admin_api, child_category
):
    result = await query_admin_api(
        CATEGORY_UPDATE_MUTATION,
        {
            "category": str(child_category.id),
            "input": {
                "parent": None,
            },
        },
    )

    assert result["data"]["categoryUpdate"] == {
        "category": {
            "id": str(child_category.id),
            "name": "Child Category",
            "slug": "child-category",
            "icon": None,
            "color": "#0F0",
            "parent": None,
            "isClosed": False,
        },
        "errors": None,
    }

    category_from_db = await child_category.refresh_from_db()
    assert category_from_db.parent_id is None
    assert category_from_db.depth == 0
    assert category_from_db.left == 9
    assert category_from_db.right == 10

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
    result = await query_admin_api(
        CATEGORY_UPDATE_MUTATION,
        {
            "category": str(sibling_category.id),
            "input": {
                "parent": str(category.id),
            },
        },
    )

    assert result["data"]["categoryUpdate"] == {
        "category": {
            "id": str(sibling_category.id),
            "name": "Sibling Category",
            "slug": "sibling-category",
            "icon": None,
            "color": "#0F0",
            "parent": {
                "id": str(category.id),
            },
            "isClosed": False,
        },
        "errors": None,
    }

    category_from_db = await sibling_category.refresh_from_db()
    assert category_from_db.parent_id == category.id
    assert category_from_db.depth == 1
    assert category_from_db.left == 6
    assert category_from_db.right == 7

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
async def test_category_update_mutation_fails_if_category_id_is_invalid(
    query_admin_api,
):
    result = await query_admin_api(
        CATEGORY_UPDATE_MUTATION,
        {
            "category": "invalid",
            "input": {
                "name": "Edited category",
            },
        },
    )

    assert result["data"]["categoryUpdate"] == {
        "category": None,
        "errors": [
            {
                "location": ["category"],
                "type": "type_error.integer",
            }
        ],
    }


@pytest.mark.asyncio
async def test_category_update_mutation_fails_if_category_doesnt_exist(query_admin_api):
    result = await query_admin_api(
        CATEGORY_UPDATE_MUTATION,
        {
            "category": "4000",
            "input": {
                "name": "Edited category",
            },
        },
    )

    assert result["data"]["categoryUpdate"] == {
        "category": None,
        "errors": [
            {
                "location": ["category"],
                "type": "value_error.category.not_exists",
            }
        ],
    }


@pytest.mark.asyncio
async def test_category_update_mutation_fails_if_category_name_is_too_short(
    query_admin_api, category
):
    result = await query_admin_api(
        CATEGORY_UPDATE_MUTATION,
        {
            "category": str(category.id),
            "input": {
                "name": "   ",
            },
        },
    )

    assert result["data"]["categoryUpdate"] == {
        "category": {
            "id": str(category.id),
            "name": "Category",
            "slug": "category",
            "icon": None,
            "color": "#0F0",
            "parent": None,
            "isClosed": False,
        },
        "errors": [
            {
                "location": ["name"],
                "type": "value_error.any_str.min_length",
            }
        ],
    }


@pytest.mark.asyncio
async def test_category_update_mutation_fails_if_category_name_is_too_long(
    query_admin_api, category
):
    result = await query_admin_api(
        CATEGORY_UPDATE_MUTATION,
        {
            "category": str(category.id),
            "input": {
                "name": "a" * 256,
            },
        },
    )

    assert result["data"]["categoryUpdate"] == {
        "category": {
            "id": str(category.id),
            "name": "Category",
            "slug": "category",
            "icon": None,
            "color": "#0F0",
            "parent": None,
            "isClosed": False,
        },
        "errors": [
            {
                "location": ["name"],
                "type": "value_error.any_str.max_length",
            }
        ],
    }


@pytest.mark.asyncio
async def test_category_update_mutation_fails_if_category_name_is_not_sluggable(
    query_admin_api, category
):
    result = await query_admin_api(
        CATEGORY_UPDATE_MUTATION,
        {
            "category": str(category.id),
            "input": {
                "name": "!!!!",
            },
        },
    )

    assert result["data"]["categoryUpdate"] == {
        "category": {
            "id": str(category.id),
            "name": "Category",
            "slug": "category",
            "icon": None,
            "color": "#0F0",
            "parent": None,
            "isClosed": False,
        },
        "errors": [
            {
                "location": ["name"],
                "type": "value_error.str.regex",
            }
        ],
    }


@pytest.mark.asyncio
async def test_category_update_mutation_fails_if_category_parent_is_invalid(
    query_admin_api, sibling_category
):
    result = await query_admin_api(
        CATEGORY_UPDATE_MUTATION,
        {
            "category": str(sibling_category.id),
            "input": {
                "parent": "invalid",
            },
        },
    )

    assert result["data"]["categoryUpdate"] == {
        "category": {
            "id": str(sibling_category.id),
            "name": "Sibling Category",
            "slug": "sibling-category",
            "icon": None,
            "color": "#0F0",
            "parent": None,
            "isClosed": False,
        },
        "errors": [
            {
                "location": ["parent"],
                "type": "type_error.integer",
            }
        ],
    }


@pytest.mark.asyncio
async def test_category_update_mutation_fails_if_category_parent_doesnt_exist(
    query_admin_api, sibling_category
):
    result = await query_admin_api(
        CATEGORY_UPDATE_MUTATION,
        {
            "category": str(sibling_category.id),
            "input": {
                "parent": "4000",
            },
        },
    )

    assert result["data"]["categoryUpdate"] == {
        "category": {
            "id": str(sibling_category.id),
            "name": "Sibling Category",
            "slug": "sibling-category",
            "icon": None,
            "color": "#0F0",
            "parent": None,
            "isClosed": False,
        },
        "errors": [
            {
                "location": ["parent"],
                "type": "value_error.category.not_exists",
            }
        ],
    }


@pytest.mark.asyncio
async def test_category_update_mutation_fails_if_category_parent_is_category(
    query_admin_api, sibling_category
):
    result = await query_admin_api(
        CATEGORY_UPDATE_MUTATION,
        {
            "category": str(sibling_category.id),
            "input": {
                "parent": str(sibling_category.id),
            },
        },
    )

    assert result["data"]["categoryUpdate"] == {
        "category": {
            "id": str(sibling_category.id),
            "name": "Sibling Category",
            "slug": "sibling-category",
            "icon": None,
            "color": "#0F0",
            "parent": None,
            "isClosed": False,
        },
        "errors": [
            {
                "location": ["parent"],
                "type": "value_error.category.invalid_parent",
            }
        ],
    }


@pytest.mark.asyncio
async def test_category_update_mutation_fails_if_parent_is_child_category(
    query_admin_api, child_category, sibling_category
):
    result = await query_admin_api(
        CATEGORY_UPDATE_MUTATION,
        {
            "category": str(sibling_category.id),
            "input": {
                "parent": str(child_category.id),
            },
        },
    )

    assert result["data"]["categoryUpdate"] == {
        "category": {
            "id": str(sibling_category.id),
            "name": "Sibling Category",
            "slug": "sibling-category",
            "icon": None,
            "color": "#0F0",
            "parent": None,
            "isClosed": False,
        },
        "errors": [
            {
                "location": ["parent"],
                "type": "value_error.category.invalid_parent",
            }
        ],
    }


@pytest.mark.asyncio
async def test_category_update_mutation_fails_if_category_has_children(
    query_admin_api, category, sibling_category
):
    result = await query_admin_api(
        CATEGORY_UPDATE_MUTATION,
        {
            "category": str(category.id),
            "input": {
                "parent": str(sibling_category.id),
            },
        },
    )

    assert result["data"]["categoryUpdate"] == {
        "category": {
            "id": str(category.id),
            "name": "Category",
            "slug": "category",
            "icon": None,
            "color": "#0F0",
            "parent": None,
            "isClosed": False,
        },
        "errors": [
            {
                "location": ["parent"],
                "type": "value_error.category.invalid_parent",
            }
        ],
    }


@pytest.mark.asyncio
async def test_category_update_mutation_requires_admin_auth(query_admin_api, category):
    result = await query_admin_api(
        CATEGORY_UPDATE_MUTATION,
        {
            "category": str(category.id),
            "input": {"name": "Updated Category"},
        },
        include_auth=False,
        expect_error=True,
    )

    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"] is None
