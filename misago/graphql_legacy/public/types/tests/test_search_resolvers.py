import pytest

SEARCH_QUERY = """
    query Search($query: String!) {
        search(query: $query) {
            users {
                id
                name
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_search_users_query_returns_user_matching_query(
    query_public_api, admin, user
):
    result = await query_public_api(SEARCH_QUERY, {"query": admin.slug})
    assert result["data"]["search"]["users"] == [
        {
            "id": str(admin.id),
            "name": admin.name,
        }
    ]


@pytest.mark.asyncio
async def test_search_users_query_returns_user_partially_matching_query(
    query_public_api, moderator, user
):
    result = await query_public_api(SEARCH_QUERY, {"query": "mod"})
    assert result["data"]["search"]["users"] == [
        {
            "id": str(moderator.id),
            "name": moderator.name,
        }
    ]


@pytest.mark.asyncio
async def test_search_users_query_returns_empty_list_for_no_results(
    query_public_api, user
):
    result = await query_public_api(SEARCH_QUERY, {"query": "mod"})
    assert result["data"]["search"]["users"] == []
