import pytest

AUTH_QUERY = """
    query Auth {
        auth {
            id
            name
        }
    }
"""


@pytest.mark.asyncio
async def test_auth_query_is_resolved_to_authenticated_admin(query_admin_api, admin):
    result = await query_admin_api(AUTH_QUERY)
    assert result["data"]["auth"]["id"] == str(admin.id)
    assert result["data"]["auth"]["name"] == admin.name


@pytest.mark.asyncio
async def test_auth_query_is_resolved_to_none_for_unauthenticated_client(
    query_admin_api, admin
):
    result = await query_admin_api(AUTH_QUERY, include_auth=False)
    assert result["data"]["auth"] is None
