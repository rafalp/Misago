import pytest

THREAD_QUERY = """
    query GetThread($thread: ID!) {
        thread(id: $thread) {
            id
            title
            startedAt
            lastPostedAt
            category {
                id
                name
            }
            firstPost {
                id
            }
            starter {
                id
                name
            }
            lastPoster {
                id
                name
            }
            lastPost {
                id
            }
            lastPostUrl
            lastPostUrlAbsolute: lastPostUrl(absolute: true)
        }
    }
"""


@pytest.mark.asyncio
async def test_thread_query_is_resolved_by_id(query_public_api, thread):
    result = await query_public_api(THREAD_QUERY, {"thread": str(thread.id)})
    assert result["data"]["thread"]["id"] == str(thread.id)
    assert result["data"]["thread"]["title"] == thread.title


@pytest.mark.asyncio
async def test_thread_query_is_resolved_to_none_for_nonexisting_thread(
    query_public_api, thread
):
    result = await query_public_api(THREAD_QUERY, {"thread": str(thread.id * 100)})
    assert result["data"]["thread"] is None


@pytest.mark.asyncio
async def test_thread_category_is_resolved(query_public_api, thread, category):
    result = await query_public_api(THREAD_QUERY, {"thread": str(thread.id)})
    assert result["data"]["thread"]["category"] == {
        "id": str(category.id),
        "name": category.name,
    }


@pytest.mark.asyncio
async def test_thread_starter_is_resolved(query_public_api, thread, user):
    await thread.update(starter=user)

    result = await query_public_api(THREAD_QUERY, {"thread": str(thread.id)})
    assert result["data"]["thread"]["starter"] == {
        "id": str(user.id),
        "name": user.name,
    }


@pytest.mark.asyncio
async def test_thread_starter_is_resolved_to_none_is_user_is_deleted(
    query_public_api, thread
):
    await thread.update(starter=False)

    result = await query_public_api(THREAD_QUERY, {"thread": str(thread.id)})
    assert result["data"]["thread"]["starter"] is None


@pytest.mark.asyncio
async def test_thread_starter_is_resolved_to_none_is_user_is_inactive(
    query_public_api, thread, user
):
    await thread.update(starter=user)
    await user.update(is_active=False)

    result = await query_public_api(THREAD_QUERY, {"thread": str(thread.id)})
    assert result["data"]["thread"]["starter"] is None


@pytest.mark.asyncio
async def test_thread_last_poster_is_resolved(query_public_api, thread, user):
    await thread.update(last_poster=user)

    result = await query_public_api(THREAD_QUERY, {"thread": str(thread.id)})
    assert result["data"]["thread"]["lastPoster"] == {
        "id": str(user.id),
        "name": user.name,
    }


@pytest.mark.asyncio
async def test_thread_last_poster_is_resolved_to_none_if_user_is_deletedd(
    query_public_api, thread
):
    await thread.update(last_poster=False)

    result = await query_public_api(THREAD_QUERY, {"thread": str(thread.id)})
    assert result["data"]["thread"]["lastPoster"] is None


@pytest.mark.asyncio
async def test_thread_last_poster_is_resolved_to_none_is_user_is_inactive(
    query_public_api, thread, user
):
    await thread.update(last_poster=user)
    await user.update(is_active=False)

    result = await query_public_api(THREAD_QUERY, {"thread": str(thread.id)})
    assert result["data"]["thread"]["lastPoster"] is None


@pytest.mark.asyncio
async def test_thread_first_post_is_resolved(query_public_api, thread, post):
    result = await query_public_api(THREAD_QUERY, {"thread": str(thread.id)})
    assert result["data"]["thread"]["firstPost"] == {"id": str(post.id)}


@pytest.mark.asyncio
async def test_thread_last_post_is_resolved(query_public_api, thread, post):
    result = await query_public_api(THREAD_QUERY, {"thread": str(thread.id)})
    assert result["data"]["thread"]["lastPost"] == {"id": str(post.id)}


@pytest.mark.asyncio
async def test_thread_last_post_url_is_resolved(query_public_api, thread, post):
    result = await query_public_api(THREAD_QUERY, {"thread": str(thread.id)})
    assert result["data"]["thread"]["lastPostUrl"] == (
        f"/t/{thread.slug}/{thread.id}/#post-{post.id}"
    )


@pytest.mark.asyncio
async def test_thread_last_post_absolute_url_is_resolved(
    query_public_api, thread, post
):
    result = await query_public_api(THREAD_QUERY, {"thread": str(thread.id)})
    assert result["data"]["thread"]["lastPostUrlAbsolute"] == (
        f"http://example.com/t/{thread.slug}/{thread.id}/#post-{post.id}"
    )
