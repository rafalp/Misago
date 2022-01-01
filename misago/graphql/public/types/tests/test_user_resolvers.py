import pytest


USER_QUERY = """
    query GetUser($user: ID!) {
        user(id: $user) {
            id
            name
        }
    }
"""


@pytest.mark.asyncio
async def test_user_query_is_resolved_by_id(query_public_api, user):
    result = await query_public_api(USER_QUERY, {"user": str(user.id)})
    assert result["data"]["user"] == {
        "id": str(user.id),
        "name": user.name,
    }


@pytest.mark.asyncio
async def test_user_query_is_resolved_to_none_for_nonexisting_user(
    query_public_api, user
):
    result = await query_public_api(USER_QUERY, {"user": str(user.id * 1000)})
    assert result["data"]["user"] is None


@pytest.mark.asyncio
async def test_user_query_is_resolved_to_none_for_inactive_user(query_public_api, user):
    await user.update(is_active=False)
    result = await query_public_api(USER_QUERY, {"user": str(user.id * 1000)})
    assert result["data"]["user"] is None
