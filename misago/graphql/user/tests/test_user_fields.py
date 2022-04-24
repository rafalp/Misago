import pytest

USER_IS_ACTIVE_QUERY = """
    query User($id: ID!) {
        user(id: $id) {
            id
            isActive
        }
    }
"""


@pytest.mark.asyncio
async def test_admin_schema_user_is_active_field(query_admin_api, admin, inactive_user):
    result = await query_admin_api(USER_IS_ACTIVE_QUERY, {"id": admin.id})
    assert result["data"]["user"]["id"] == str(admin.id)
    assert result["data"]["user"]["isActive"] is True

    result = await query_admin_api(USER_IS_ACTIVE_QUERY, {"id": inactive_user.id})
    assert result["data"]["user"]["id"] == str(inactive_user.id)
    assert result["data"]["user"]["isActive"] is False
