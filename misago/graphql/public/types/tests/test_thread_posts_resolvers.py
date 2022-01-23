import pytest

THREAD_POSTS_QUERY = """
    query GetThreadPosts($thread: ID!, $page: Int) {
        thread(id: $thread) {
            id
            posts {
                page(page: $page) {
                    items {
                        id
                    }
                    number
                }
                pagination {
                    count
                    pages
                }
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_thread_posts_first_page_is_resolved_by_default(
    query_public_api, thread, post
):
    result = await query_public_api(THREAD_POSTS_QUERY, {"thread": str(thread.id)})
    assert result["data"]["thread"] == {
        "id": str(thread.id),
        "posts": {
            "page": {
                "items": [
                    {
                        "id": str(post.id),
                    }
                ],
                "number": 1,
            },
            "pagination": {
                "count": 1,
                "pages": 1,
            },
        },
    }


@pytest.mark.asyncio
async def test_thread_posts_page_is_resolved_by_number(query_public_api, thread, post):
    result = await query_public_api(
        THREAD_POSTS_QUERY, {"thread": str(thread.id), "page": 1}
    )
    assert result["data"]["thread"] == {
        "id": str(thread.id),
        "posts": {
            "page": {
                "items": [
                    {
                        "id": str(post.id),
                    }
                ],
                "number": 1,
            },
            "pagination": {
                "count": 1,
                "pages": 1,
            },
        },
    }


@pytest.mark.asyncio
async def test_thread_posts_page_is_resolved_to_none_for_too_big_page(
    query_public_api, thread
):
    result = await query_public_api(
        THREAD_POSTS_QUERY, {"thread": str(thread.id), "page": 100}
    )
    assert result["data"]["thread"] == {
        "id": str(thread.id),
        "posts": {
            "page": None,
            "pagination": {
                "count": 1,
                "pages": 1,
            },
        },
    }


THREAD_POST_QUERY = """
    query GetThreadPost($thread: ID!, $post: ID!) {
        thread(id: $thread) {
            id
            post(id: $post) {
                id
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_thread_post_is_resolved_by_id(query_public_api, thread, post):
    result = await query_public_api(
        THREAD_POST_QUERY, {"thread": str(thread.id), "post": str(post.id)}
    )
    assert result["data"]["thread"]["post"] == {
        "id": str(post.id),
    }


@pytest.mark.asyncio
async def test_thread_post_is_resolved_to_none_for_post_in_other_thread(
    query_public_api, thread, user_post
):
    result = await query_public_api(
        THREAD_POST_QUERY, {"thread": str(thread.id), "post": str(user_post.id)}
    )
    assert result["data"]["thread"]["post"] is None


@pytest.mark.asyncio
async def test_thread_post_is_resolved_to_none_for_nonexistant_post(
    query_public_api, thread, post
):
    result = await query_public_api(
        THREAD_POST_QUERY, {"thread": str(thread.id), "post": str(post.id * 100)}
    )
    assert result["data"]["thread"]["post"] is None
