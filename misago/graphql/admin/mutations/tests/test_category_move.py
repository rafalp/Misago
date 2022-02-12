from unittest.mock import ANY

import pytest

from .....categories.get import get_all_categories

CATEGORY_MOVE_MUTATION = """
    mutation CategoryMove(
        $category: ID!, $parent: ID, $before: ID
    ) {
        categoryMove(
            category: $category,
            parent: $parent,
            before: $before
        ) {
            category {
                id
                parent {
                    id
                }
            }
            categories {
                id
                depth
            }
            errors {
                location
                type
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_move_category_mutation_moves_sibling_category_before_other_category(
    query_admin_api, category, child_category, sibling_category, closed_category
):
    result = await query_admin_api(
        CATEGORY_MOVE_MUTATION,
        {
            "category": str(sibling_category.id),
            "before": str(category.id),
        },
    )

    assert result["data"]["categoryMove"] == {
        "category": {
            "id": str(sibling_category.id),
            "parent": None,
        },
        "categories": [
            ANY,
            {
                "id": str(sibling_category.id),
                "depth": 0,
            },
            {
                "id": str(category.id),
                "depth": 0,
            },
            {
                "id": str(child_category.id),
                "depth": 1,
            },
            {
                "id": str(closed_category.id),
                "depth": 0,
            },
        ],
        "errors": None,
    }

    category_from_db = await sibling_category.fetch_from_db()
    assert category_from_db.parent_id is None
    assert category_from_db.depth == 0
    assert category_from_db.left == 3
    assert category_from_db.right == 4

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
    query_admin_api, category, child_category, sibling_category, closed_category
):
    result = await query_admin_api(
        CATEGORY_MOVE_MUTATION,
        {
            "category": str(sibling_category.id),
            "parent": str(category.id),
            "before": str(child_category.id),
        },
    )

    assert result["data"]["categoryMove"] == {
        "category": {
            "id": str(sibling_category.id),
            "parent": {
                "id": str(category.id),
            },
        },
        "categories": [
            ANY,  # Default category
            {
                "id": str(category.id),
                "depth": 0,
            },
            {
                "id": str(sibling_category.id),
                "depth": 1,
            },
            {
                "id": str(child_category.id),
                "depth": 1,
            },
            {
                "id": str(closed_category.id),
                "depth": 0,
            },
        ],
        "errors": None,
    }

    category_from_db = await sibling_category.fetch_from_db()
    assert category_from_db.parent_id == category.id
    assert category_from_db.depth == 1
    assert category_from_db.left == 4
    assert category_from_db.right == 5

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
    query_admin_api, category, child_category, sibling_category, closed_category
):
    result = await query_admin_api(
        CATEGORY_MOVE_MUTATION,
        {
            "category": str(sibling_category.id),
            "parent": str(category.id),
        },
    )

    assert result["data"]["categoryMove"] == {
        "category": {
            "id": str(sibling_category.id),
            "parent": {
                "id": str(category.id),
            },
        },
        "categories": [
            ANY,  # Default category
            {
                "id": str(category.id),
                "depth": 0,
            },
            {
                "id": str(child_category.id),
                "depth": 1,
            },
            {
                "id": str(sibling_category.id),
                "depth": 1,
            },
            {
                "id": str(closed_category.id),
                "depth": 0,
            },
        ],
        "errors": None,
    }

    category_from_db = await sibling_category.fetch_from_db()
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
        (1, 4, 5),  # Child category
        (1, 6, 7),  # Sibling category
        (0, 9, 10),  # Closed category
    ]


@pytest.mark.asyncio
async def test_move_category_mutation_moves_child_category_to_root(
    query_admin_api, category, child_category, sibling_category, closed_category
):
    result = await query_admin_api(
        CATEGORY_MOVE_MUTATION,
        {
            "category": str(child_category.id),
        },
    )

    assert result["data"]["categoryMove"] == {
        "category": {
            "id": str(child_category.id),
            "parent": None,
        },
        "categories": [
            ANY,  # Default category
            {
                "id": str(category.id),
                "depth": 0,
            },
            {
                "id": str(sibling_category.id),
                "depth": 0,
            },
            {
                "id": str(closed_category.id),
                "depth": 0,
            },
            {
                "id": str(child_category.id),
                "depth": 0,
            },
        ],
        "errors": None,
    }

    category_from_db = await child_category.fetch_from_db()
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
async def test_move_category_mutation_moves_child_category_to_root_before_parent(
    query_admin_api, category, child_category, sibling_category, closed_category
):
    result = await query_admin_api(
        CATEGORY_MOVE_MUTATION,
        {
            "category": str(child_category.id),
            "before": str(category.id),
        },
    )

    assert result["data"]["categoryMove"] == {
        "category": {
            "id": str(child_category.id),
            "parent": None,
        },
        "categories": [
            ANY,  # Default category
            {
                "id": str(child_category.id),
                "depth": 0,
            },
            {
                "id": str(category.id),
                "depth": 0,
            },
            {
                "id": str(sibling_category.id),
                "depth": 0,
            },
            {
                "id": str(closed_category.id),
                "depth": 0,
            },
        ],
        "errors": None,
    }

    category_from_db = await child_category.fetch_from_db()
    assert category_from_db.id == child_category.id
    assert category_from_db.parent_id is None
    assert category_from_db.depth == 0
    assert category_from_db.left == 3
    assert category_from_db.right == 4

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
async def test_move_category_mutation_fails_if_category_id_is_invalid(query_admin_api):
    result = await query_admin_api(
        CATEGORY_MOVE_MUTATION,
        {
            "category": "invalid",
        },
    )

    assert result["data"]["categoryMove"] == {
        "category": None,
        "categories": ANY,
        "errors": [
            {
                "location": "category",
                "type": "type_error.integer",
            }
        ],
    }


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_parent_id_is_invalid(
    query_admin_api, category
):
    result = await query_admin_api(
        CATEGORY_MOVE_MUTATION,
        {
            "category": str(category.id),
            "parent": "invalid",
        },
    )

    assert result["data"]["categoryMove"] == {
        "category": {
            "id": str(category.id),
            "parent": None,
        },
        "categories": ANY,
        "errors": [
            {
                "location": "parent",
                "type": "type_error.integer",
            }
        ],
    }


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_before_id_is_invalid(
    query_admin_api, category
):
    result = await query_admin_api(
        CATEGORY_MOVE_MUTATION,
        {
            "category": str(category.id),
            "before": "invalid",
        },
    )

    assert result["data"]["categoryMove"] == {
        "category": {
            "id": str(category.id),
            "parent": None,
        },
        "categories": ANY,
        "errors": [
            {
                "location": "before",
                "type": "type_error.integer",
            }
        ],
    }


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_category_id_doesnt_exist(
    query_admin_api,
):
    result = await query_admin_api(
        CATEGORY_MOVE_MUTATION,
        {
            "category": "4000",
        },
    )

    assert result["data"]["categoryMove"] == {
        "category": None,
        "categories": ANY,
        "errors": [
            {
                "location": "category",
                "type": "category_error.not_found",
            }
        ],
    }


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_parent_id_doesnt_exist(
    query_admin_api, category
):
    result = await query_admin_api(
        CATEGORY_MOVE_MUTATION,
        {
            "category": str(category.id),
            "parent": "4000",
        },
    )

    assert result["data"]["categoryMove"] == {
        "category": {
            "id": str(category.id),
            "parent": None,
        },
        "categories": ANY,
        "errors": [
            {
                "location": "parent",
                "type": "category_error.not_found",
            }
        ],
    }


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_before_id_doesnt_exist(
    query_admin_api, category
):
    result = await query_admin_api(
        CATEGORY_MOVE_MUTATION,
        {
            "category": str(category.id),
            "before": "4000",
        },
    )

    assert result["data"]["categoryMove"] == {
        "category": {
            "id": str(category.id),
            "parent": None,
        },
        "categories": ANY,
        "errors": [
            {
                "location": "before",
                "type": "category_error.not_found",
            }
        ],
    }


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_category_parent_is_itself(
    query_admin_api, category
):
    result = await query_admin_api(
        CATEGORY_MOVE_MUTATION,
        {
            "category": str(category.id),
            "parent": str(category.id),
        },
    )

    assert result["data"]["categoryMove"] == {
        "category": {
            "id": str(category.id),
            "parent": None,
        },
        "categories": ANY,
        "errors": [
            {
                "location": "parent",
                "type": "category_error.invalid_parent",
            }
        ],
    }


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_category_before_is_itself(
    query_admin_api, category
):
    result = await query_admin_api(
        CATEGORY_MOVE_MUTATION,
        {
            "category": str(category.id),
            "before": str(category.id),
        },
    )

    assert result["data"]["categoryMove"] == {
        "category": {
            "id": str(category.id),
            "parent": None,
        },
        "categories": ANY,
        "errors": [
            {
                "location": "before",
                "type": "category_error.invalid_parent",
            }
        ],
    }


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_parent_is_child_category(
    query_admin_api, category, child_category
):
    result = await query_admin_api(
        CATEGORY_MOVE_MUTATION,
        {
            "category": str(category.id),
            "parent": str(child_category.id),
        },
    )

    assert result["data"]["categoryMove"] == {
        "category": {
            "id": str(category.id),
            "parent": None,
        },
        "categories": ANY,
        "errors": [
            {
                "location": "parent",
                "type": "category_error.invalid_parent",
            }
        ],
    }


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_root_category_is_moved_after_child(
    query_admin_api, category, child_category
):
    result = await query_admin_api(
        CATEGORY_MOVE_MUTATION,
        {
            "category": str(category.id),
            "before": str(child_category.id),
        },
    )

    assert result["data"]["categoryMove"] == {
        "category": {
            "id": str(category.id),
            "parent": None,
        },
        "categories": ANY,
        "errors": [
            {
                "location": "before",
                "type": "category_error.invalid_parent",
            }
        ],
    }


@pytest.mark.asyncio
async def test_move_category_mutation_fails_if_child_is_moved_after_root(
    query_admin_api, category, child_category, sibling_category
):
    result = await query_admin_api(
        CATEGORY_MOVE_MUTATION,
        {
            "category": str(child_category.id),
            "parent": str(category.id),
            "before": str(sibling_category.id),
        },
    )

    assert result["data"]["categoryMove"] == {
        "category": {
            "id": str(child_category.id),
            "parent": {
                "id": str(category.id),
            },
        },
        "categories": ANY,
        "errors": [
            {
                "location": "before",
                "type": "category_error.invalid_parent",
            }
        ],
    }


@pytest.mark.asyncio
async def test_category_move_mutation_requires_admin_auth(query_admin_api, category):
    result = await query_admin_api(
        CATEGORY_MOVE_MUTATION,
        {
            "category": str(category.id),
        },
        include_auth=False,
        expect_error=True,
    )

    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"] is None
