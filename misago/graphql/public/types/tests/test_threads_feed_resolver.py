import pytest


THREADS_FEED_QUERY = """
    query GetThreads($category: ID, $user: ID) {
        threads(category: $category, user: $user) {
            items {
                id
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_threads_query_resolves_to_empty_list(query_public_api, db):
    result = await query_public_api(THREADS_FEED_QUERY)
    assert result["data"]["threads"] == {
        "items": [],
    }


@pytest.mark.asyncio
async def test_threads_query_resolves_to_threads_list(query_public_api, thread):
    result = await query_public_api(THREADS_FEED_QUERY)
    assert result["data"]["threads"] == {
        "items": [
            {
                "id": str(thread.id),
            },
        ],
    }


@pytest.mark.asyncio
async def test_threads_query_resolves_to_category_threads_list(
    query_public_api, category, thread, closed_category_thread
):
    result = await query_public_api(THREADS_FEED_QUERY, {"category": str(category.id)})
    assert result["data"]["threads"] == {
        "items": [
            {
                "id": str(thread.id),
            },
        ],
    }


@pytest.mark.asyncio
async def test_threads_query_resolves_to_empty_list_for_nonexistant_category(
    query_public_api, category, thread
):
    result = await query_public_api(
        THREADS_FEED_QUERY, {"category": str(category.id * 100)}
    )
    assert result["data"]["threads"] == {
        "items": [],
    }


@pytest.mark.asyncio
async def test_threads_query_resolves_to_user_threads_list(
    query_public_api, thread, user_thread, user
):
    result = await query_public_api(THREADS_FEED_QUERY, {"user": str(user.id)})
    assert result["data"]["threads"] == {
        "items": [
            {
                "id": str(user_thread.id),
            },
        ],
    }


@pytest.mark.asyncio
async def test_threads_query_resolves_to_empty_list_for_nonexistant_user(
    query_public_api, thread, user_thread, user
):
    result = await query_public_api(THREADS_FEED_QUERY, {"user": str(user.id * 100)})
    assert result["data"]["threads"] == {
        "items": [
            {
                "id": str(user_thread.id),
            },
        ],
    }
