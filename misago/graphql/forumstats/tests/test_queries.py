import pytest

FORUM_STATS_ID_QUERY = """
    {
        forumStats {
            id
            threads
            posts
            users
        }
    }
"""


@pytest.mark.asyncio
async def test_forum_stats_id_resolves_to_random_value(
    query_public_api, db, user, thread, post
):
    result = await query_public_api(FORUM_STATS_ID_QUERY)
    assert result["data"]["forumStats"]["id"]

    other_result = await query_public_api(FORUM_STATS_ID_QUERY)
    previous_id = result["data"]["forumStats"]["id"]
    assert other_result["data"]["forumStats"]["id"] != previous_id


FORUM_STATS_QUERY = """
    {
        forumStats {
            threads
            posts
            users
        }
    }
"""


@pytest.mark.asyncio
async def test_forum_stats_query_returns_current_stats(
    query_public_api, db, user, thread, post
):
    result = await query_public_api(FORUM_STATS_QUERY)
    assert result["data"]["forumStats"] == {
        "threads": 1,
        "posts": 1,
        "users": 1,
    }
