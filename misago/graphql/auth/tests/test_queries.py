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
async def test_auth_query_resolves_to_authenticated_user(query_public_api, user):
    result = await query_public_api(AUTH_QUERY, auth=user)
    assert result["data"]["auth"] == {
        "id": str(user.id),
        "name": user.name,
    }


@pytest.mark.asyncio
async def test_auth_query_resolves_to_none_for_anonymous_user(query_public_api, db):
    result = await query_public_api(AUTH_QUERY)
    assert result["data"]["auth"] is None


@pytest.mark.asyncio
async def test_admin_schema_auth_query_is_resolved_to_authenticated_admin(
    query_admin_api, admin
):
    result = await query_admin_api(AUTH_QUERY)
    assert result["data"]["auth"]["id"] == str(admin.id)
    assert result["data"]["auth"]["name"] == admin.name


@pytest.mark.asyncio
async def test_admin_schema_auth_query_is_resolved_to_none_for_unauthenticated_client(
    query_admin_api, admin
):
    result = await query_admin_api(AUTH_QUERY, include_auth=False)
    assert result["data"]["auth"] is None
