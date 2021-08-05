import pytest

USER_QUERY = """
    query User($id: ID!) {
        user(id: $id) {
            id
        }
    }
"""


@pytest.mark.asyncio
async def test_user_query_returns_user(query_admin_api, admin):
    result = await query_admin_api(USER_QUERY, {"id": admin.id})
    assert result["data"]["user"]["id"] == str(admin.id)


@pytest.mark.asyncio
async def test_user_query_returns_none_when_user_is_not_found(query_admin_api, admin):
    result = await query_admin_api(USER_QUERY, {"id": admin.id + 1})
    assert result["data"]["user"] is None


@pytest.mark.asyncio
async def test_user_query_requires_admin_auth(query_admin_api, admin):
    result = await query_admin_api(
        USER_QUERY, {"id": admin.id}, expect_error=True, include_auth=False
    )
    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"]["user"] is None
