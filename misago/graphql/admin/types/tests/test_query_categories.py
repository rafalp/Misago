import pytest

CATEGORY_QUERY = """
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
    result = await query_admin_api(CATEGORY_QUERY)
    categories_ids = [c["id"] for c in result["data"]["categories"]]
    assert str(category.id) in categories_ids


@pytest.mark.asyncio
async def test_categories_query_requires_admin_auth(query_admin_api, categories):
    result = await query_admin_api(
        CATEGORY_QUERY, expect_error=True, include_auth=False
    )
    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"]["categories"] is None
