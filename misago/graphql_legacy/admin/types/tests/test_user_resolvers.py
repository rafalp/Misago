import pytest

USER_QUERY = """
    query User($id: ID!) {
        user(id: $id) {
            id
            name
            isActive
        }
    }
"""


@pytest.mark.asyncio
async def test_user_query_is_resolved_by_id(query_admin_api, admin):
    result = await query_admin_api(USER_QUERY, {"id": admin.id})
    assert result["data"]["user"]["id"] == str(admin.id)
    assert result["data"]["user"]["name"] == admin.name


@pytest.mark.asyncio
async def test_user_query_is_resolved_to_none_for_nonexisting_user(
    query_admin_api, admin
):
    result = await query_admin_api(USER_QUERY, {"id": admin.id + 1})
    assert result["data"]["user"] is None


@pytest.mark.asyncio
async def test_user_query_is_resolved_to_none_for_invalid_id(query_admin_api, admin):
    result = await query_admin_api(USER_QUERY, {"id": "invalid"})
    assert result["data"]["user"] is None


@pytest.mark.asyncio
async def test_user_is_active_is_resolved(query_admin_api, admin, inactive_user):
    result = await query_admin_api(USER_QUERY, {"id": admin.id})
    assert result["data"]["user"]["id"] == str(admin.id)
    assert result["data"]["user"]["isActive"] is True

    result = await query_admin_api(USER_QUERY, {"id": inactive_user.id})
    assert result["data"]["user"]["id"] == str(inactive_user.id)
    assert result["data"]["user"]["isActive"] is False


@pytest.mark.asyncio
async def test_user_query_requires_admin_auth(query_admin_api, admin):
    result = await query_admin_api(
        USER_QUERY, {"id": admin.id}, expect_error=True, include_auth=False
    )
    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"]["user"] is None
