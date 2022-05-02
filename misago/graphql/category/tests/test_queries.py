import pytest

CATEGORY_QUERY = """
    query GetCategory($category: ID!) {
        category(id: $category) {
            id
        }
    }
"""


@pytest.mark.asyncio
async def test_category_query_resolves_by_id(query_public_api, category):
    result = await query_public_api(CATEGORY_QUERY, {"category": str(category.id)})
    assert result["data"]["category"]["id"] == str(category.id)


@pytest.mark.asyncio
async def test_category_query_resolves_to_none_for_non_invalid_id(
    query_public_api, category
):
    result = await query_public_api(CATEGORY_QUERY, {"category": "invalid"})
    assert result["data"]["category"] is None


@pytest.mark.asyncio
async def test_category_query_resolves_to_none_for_non_existing_category(
    query_public_api, category
):
    result = await query_public_api(CATEGORY_QUERY, {"category": str(category.id * 10)})
    assert result["data"]["category"] is None


@pytest.mark.asyncio
async def test_admin_schema_category_query_resolves_by_id(query_admin_api, category):
    result = await query_admin_api(CATEGORY_QUERY, {"category": str(category.id)})
    assert result["data"]["category"]["id"] == str(category.id)


@pytest.mark.asyncio
async def test_admin_schema_category_query_resolves_to_none_for_non_invalid_id(
    query_admin_api, category
):
    result = await query_admin_api(CATEGORY_QUERY, {"category": "invalid"})
    assert result["data"]["category"] is None


@pytest.mark.asyncio
async def test_admin_schema_category_query_resolves_to_none_for_non_existing_category(
    query_admin_api, category
):
    result = await query_admin_api(CATEGORY_QUERY, {"category": str(category.id * 10)})
    assert result["data"]["category"] is None


@pytest.mark.asyncio
async def test_admin_schema_category_query_requires_admin_auth(
    query_admin_api, category
):
    result = await query_admin_api(
        CATEGORY_QUERY,
        {"category": str(category.id)},
        expect_error=True,
        include_auth=False,
    )
    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"]["category"] is None


CATEGORIES_QUERY = """
    query Categories {
        categories {
            id
        }
    }
"""


@pytest.mark.asyncio
async def test_categories_query_resolves_to_root_categories_list(
    query_public_api, category, child_category
):
    result = await query_public_api(CATEGORIES_QUERY)
    ids = [i["id"] for i in result["data"]["categories"]]
    assert str(category.id) in ids
    assert str(child_category.id) not in ids


@pytest.mark.asyncio
async def test_admin_schema_categories_query_resolves_to_all_categories_list(
    query_admin_api, category, child_category
):
    result = await query_admin_api(CATEGORIES_QUERY)
    ids = [i["id"] for i in result["data"]["categories"]]
    assert str(category.id) in ids
    assert str(child_category.id) in ids


@pytest.mark.asyncio
async def test_admin_schema_categories_query_requires_admin_auth(
    query_admin_api, category
):
    result = await query_admin_api(
        CATEGORIES_QUERY,
        expect_error=True,
        include_auth=False,
    )
    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"]["categories"] is None


CATEGORY_PARENT_QUERY = """
    query CategoryParent($category: ID!) {
        category(id: $category) {
            id
            parent {
                id
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_category_parent_query_resolves_to_parent_category_for_child(
    query_public_api, category, child_category
):
    result = await query_public_api(
        CATEGORY_PARENT_QUERY, {"category": str(child_category.id)}
    )
    assert result["data"]["category"] == {
        "id": str(child_category.id),
        "parent": {
            "id": str(category.id),
        },
    }


@pytest.mark.asyncio
async def test_category_parent_query_resolves_to_none_for_root_category(
    query_public_api, category, child_category
):
    result = await query_public_api(
        CATEGORY_PARENT_QUERY, {"category": str(category.id)}
    )
    assert result["data"]["category"] == {
        "id": str(category.id),
        "parent": None,
    }


@pytest.mark.asyncio
async def test_admin_schema_category_parent_query_resolves_to_parent_category_for_child(
    query_admin_api, category, child_category
):
    result = await query_admin_api(
        CATEGORY_PARENT_QUERY, {"category": str(child_category.id)}
    )
    assert result["data"]["category"] == {
        "id": str(child_category.id),
        "parent": {
            "id": str(category.id),
        },
    }


@pytest.mark.asyncio
async def test_admin_schema_category_parent_query_resolves_to_none_for_root_category(
    query_admin_api, category, child_category
):
    result = await query_admin_api(
        CATEGORY_PARENT_QUERY, {"category": str(category.id)}
    )
    assert result["data"]["category"] == {
        "id": str(category.id),
        "parent": None,
    }


CATEGORY_CHILDREN_QUERY = """
    query CategoryChildren($category: ID!) {
        category(id: $category) {
            id
            children {
                id
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_category_children_query_resolves_to_child_categories(
    query_public_api, category, child_category
):
    result = await query_public_api(
        CATEGORY_CHILDREN_QUERY, {"category": str(category.id)}
    )
    assert result["data"]["category"] == {
        "id": str(category.id),
        "children": [
            {
                "id": str(child_category.id),
            },
        ],
    }


@pytest.mark.asyncio
async def test_category_children_query_resolves_to_empty_list_for_leaf_category(
    query_public_api, sibling_category
):
    result = await query_public_api(
        CATEGORY_CHILDREN_QUERY, {"category": str(sibling_category.id)}
    )
    assert result["data"]["category"] == {
        "id": str(sibling_category.id),
        "children": [],
    }


@pytest.mark.asyncio
async def test_admin_schema_category_children_query_resolves_to_child_categories(
    query_admin_api, category, child_category
):
    result = await query_admin_api(
        CATEGORY_CHILDREN_QUERY, {"category": str(category.id)}
    )
    assert result["data"]["category"] == {
        "id": str(category.id),
        "children": [
            {
                "id": str(child_category.id),
            },
        ],
    }


@pytest.mark.asyncio
async def test_admin_schema_category_children_query_resolves_to_empty_list_for_leaf_category(
    query_admin_api, sibling_category
):
    result = await query_admin_api(
        CATEGORY_CHILDREN_QUERY, {"category": str(sibling_category.id)}
    )
    assert result["data"]["category"] == {
        "id": str(sibling_category.id),
        "children": [],
    }


CATEGORY_STATS_QUERY = """
    query CategoryStats($category: ID!) {
        category(id: $category) {
            id
            threads
            posts
            isClosed
        }
    }
"""


@pytest.mark.asyncio
async def test_category_stats_query_returns_aggregated_results_for_parent_category(
    query_public_api, category, child_category
):
    await category.update(threads=1, posts=2)
    await child_category.update(threads=2, posts=3, is_closed=True)

    result = await query_public_api(
        CATEGORY_STATS_QUERY, {"category": str(category.id)}
    )
    data = result["data"]["category"]
    assert data["id"] == str(category.id)
    assert data["threads"] == 3
    assert data["posts"] == 5
    assert data["isClosed"] is False


@pytest.mark.asyncio
async def test_category_stats_query_returns_aggregated_results_for_child_category(
    query_public_api, category, child_category
):
    await category.update(threads=1, posts=2, is_closed=True)
    await child_category.update(threads=2, posts=3)

    result = await query_public_api(
        CATEGORY_STATS_QUERY, {"category": str(child_category.id)}
    )
    data = result["data"]["category"]
    assert data["id"] == str(child_category.id)
    assert data["threads"] == 2
    assert data["posts"] == 3
    assert data["isClosed"] is True


@pytest.mark.asyncio
async def test_admin_schema_category_stats_query_is_not_aggregating_for_parent_category(
    query_admin_api, category, child_category
):
    await category.update(threads=1, posts=2)
    await child_category.update(threads=2, posts=3, is_closed=True)

    result = await query_admin_api(CATEGORY_STATS_QUERY, {"category": str(category.id)})
    data = result["data"]["category"]
    assert data["id"] == str(category.id)
    assert data["threads"] == 1
    assert data["posts"] == 2
    assert data["isClosed"] is False


@pytest.mark.asyncio
async def test_admin_schema_category_stats_query_is_not_aggregating_for_child_category(
    query_admin_api, category, child_category
):
    await category.update(threads=1, posts=2, is_closed=True)
    await child_category.update(threads=2, posts=3)

    result = await query_admin_api(
        CATEGORY_STATS_QUERY, {"category": str(child_category.id)}
    )
    data = result["data"]["category"]
    assert data["id"] == str(child_category.id)
    assert data["threads"] == 2
    assert data["posts"] == 3
    assert data["isClosed"] is False
