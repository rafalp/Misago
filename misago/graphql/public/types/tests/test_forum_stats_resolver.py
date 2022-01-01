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
async def test_query_forum_stats_query_resolves_random_id(
    query_public_api, db, user, thread, post
):
    result = await query_public_api(FORUM_STATS_QUERY)
    assert result["data"]["forumStats"]["id"]


@pytest.mark.asyncio
async def test_query_forum_stats_query_resolves_forum_stats(
    query_public_api, db, user, thread, post
):
    result = await query_public_api(FORUM_STATS_QUERY)
    assert result["data"]["forumStats"] == {
        "id": ANY,
        "threads": 1,
        "posts": 1,
        "users": 1,
    }
