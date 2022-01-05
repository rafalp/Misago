import pytest

CATEGORIES_QUERY = """
    query Categories {
        categories {
            id
            children {
                id
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_categories_query_returns_root_categories(
    query_admin_api, categories, category
):
    result = await query_admin_api(CATEGORIES_QUERY)
    categories_ids = [c["id"] for c in result["data"]["categories"]]
    assert str(category.id) in categories_ids


@pytest.mark.asyncio
async def test_categories_query_requires_admin_auth(query_admin_api, categories):
    result = await query_admin_api(
        CATEGORIES_QUERY, expect_error=True, include_auth=False
    )
    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"]["categories"] is None


CATEGORY_QUERY = """
    query Category($id: ID!) {
        category(id: $id) {
            id
        }
    }
"""


@pytest.mark.asyncio
async def test_category_query_returns_category(query_admin_api, category):
    result = await query_admin_api(CATEGORY_QUERY, {"id": category.id})
    assert result["data"]["category"]["id"] == str(category.id)


@pytest.mark.asyncio
async def test_category_query_returns_none_when_category_is_not_found(
    query_admin_api, category
):
    result = await query_admin_api(CATEGORY_QUERY, {"id": category.id + 100})
    assert result["data"]["category"] is None


@pytest.mark.asyncio
async def test_category_query_requires_admin_auth(query_admin_api, category):
    result = await query_admin_api(
        CATEGORY_QUERY,
        {"id": category.id + 100},
        expect_error=True,
        include_auth=False,
    )
    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"]["category"] is None
