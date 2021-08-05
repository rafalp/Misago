import pytest

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
async def test_category_query_requires_admin_auth(query_admin_api, admin):
    result = await query_admin_api(
        CATEGORY_QUERY, {"id": admin.id}, expect_error=True, include_auth=False
    )
    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"]["category"] is None
