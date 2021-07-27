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
    assert "errors" not in result
    assert result["data"]["user"]["id"] == str(admin.id)


@pytest.mark.asyncio
async def test_user_query_returns_none_when_user_is_not_found(query_admin_api, admin):
    result = await query_admin_api(USER_QUERY, {"id": admin.id + 1})
    assert "errors" not in result
    assert result["data"]["user"] is None


@pytest.mark.asyncio
async def test_user_query_returns_none_when_client_is_not_authenticated(
    query_admin_api, admin
):
    result = await query_admin_api(USER_QUERY, {"id": admin.id}, include_auth=False)
    assert "errors" not in result
    assert result["data"]["user"] is None
