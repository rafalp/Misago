import pytest

AUTH_QUERY = """
    query GetAuth {
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
