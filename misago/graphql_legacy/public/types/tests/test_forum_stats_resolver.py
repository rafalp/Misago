from unittest.mock import ANY

import pytest

FORUM_STATS_QUERY = """
    query ForumStats {
        forumStats {
            id
            threads
            posts
            users
        }
    }
"""


@pytest.mark.asyncio
async def test_forum_stats_id_resolves_to_randomm_value(
    query_public_api, db, user, thread, post
):
    result = await query_public_api(FORUM_STATS_QUERY)
    assert result["data"]["forumStats"]["id"]

    other_result = await query_public_api(FORUM_STATS_QUERY)
    previous_id = result["data"]["forumStats"]["id"]
    assert other_result["data"]["forumStats"]["id"] != previous_id


@pytest.mark.asyncio
async def test_forum_stats_values_are_resolved(
    query_public_api, db, user, thread, post
):
    result = await query_public_api(FORUM_STATS_QUERY)
    assert result["data"]["forumStats"] == {
        "id": ANY,
        "threads": 1,
        "posts": 1,
        "users": 1,
    }
