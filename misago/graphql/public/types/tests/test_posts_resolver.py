import pytest

POSTS_QUERY = """
    query GetPosts($thread: ID!, $page: Int) {
        posts(thread: $thread, page: $page) {
            totalCount
            totalPages
            results {
                id
            }
            pageInfo {
                number
                hasNext
                hasPrevious
                next
                previous
                start
                stop
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_posts_query_resolves_to_first_posts_page(query_public_api, thread, post):
    result = await query_public_api(POSTS_QUERY, {"thread": str(thread.id)})
    assert result["data"]["posts"] == {
        "totalCount": 1,
        "totalPages": 1,
        "results": [
            {
                "id": str(post.id),
            },
        ],
        "pageInfo": {
            "number": 1,
            "hasNext": False,
            "hasPrevious": False,
            "next": None,
            "previous": None,
            "start": 1,
            "stop": 1,
        },
    }


@pytest.mark.asyncio
async def test_posts_query_resolves_to_specified_posts_page(
    query_public_api, thread, post
):
    result = await query_public_api(POSTS_QUERY, {"thread": str(thread.id), "page": 1})
    assert result["data"]["posts"] == {
        "totalCount": 1,
        "totalPages": 1,
        "results": [
            {
                "id": str(post.id),
            },
        ],
        "pageInfo": {
            "number": 1,
            "hasNext": False,
            "hasPrevious": False,
            "next": None,
            "previous": None,
            "start": 1,
            "stop": 1,
        },
    }


@pytest.mark.asyncio
async def test_posts_query_resolves_to_empty_page(query_public_api, thread, post):
    result = await query_public_api(POSTS_QUERY, {"thread": str(thread.id), "page": 10})
    assert result["data"]["posts"] == {
        "totalCount": 1,
        "totalPages": 1,
        "results": [],
        "pageInfo": {
            "number": 10,
            "hasNext": False,
            "hasPrevious": True,
            "next": None,
            "previous": 1,
            "start": 0,
            "stop": 0,
        },
    }


@pytest.mark.asyncio
async def test_posts_query_resolves_to_none_for_negative_page(query_public_api, thread):
    result = await query_public_api(POSTS_QUERY, {"thread": str(thread.id), "page": -1})
    assert result["data"]["posts"] is None


@pytest.mark.asyncio
async def test_posts_query_resolves_to_none_for_invalid_thread(query_public_api, db):
    result = await query_public_api(POSTS_QUERY, {"thread": "invalid"})
    assert result["data"]["posts"] is None
