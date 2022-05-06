import pytest

POST_QUERY = """
    query GetPost($post: ID!) {
        post(id: $post) {
            id
        }
    }
"""


@pytest.mark.asyncio
async def test_post_query_is_resolved_by_id(query_public_api, user_post):
    result = await query_public_api(POST_QUERY, {"post": str(user_post.id)})
    assert result["data"]["post"]["id"] == str(user_post.id)


@pytest.mark.asyncio
async def test_post_query_resolves_to_none_for_nonexisting_post(
    query_public_api, user_post
):
    result = await query_public_api(POST_QUERY, {"post": str(user_post.id * 1000)})
    assert result["data"]["post"] is None


@pytest.mark.asyncio
async def test_post_query_resolves_to_none_for_invalid_id(query_public_api, db):
    result = await query_public_api(POST_QUERY, {"post": "invalid"})
    assert result["data"]["post"] is None


POST_POSTER_QUERY = """
    query GetPostPoster($post: ID!) {
        post(id: $post) {
            id
            poster {
                id
                name
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_post_poster_is_resolved(query_public_api, user_post, user):
    result = await query_public_api(POST_POSTER_QUERY, {"post": str(user_post.id)})
    assert result["data"]["post"]["poster"] == {
        "id": str(user.id),
        "name": user.name,
    }


@pytest.mark.asyncio
async def test_post_poster_resolves_to_null_if_user_is_inactive(
    query_public_api, user_post, user
):
    await user.update(is_active=False)

    result = await query_public_api(POST_POSTER_QUERY, {"post": str(user_post.id)})
    assert result["data"]["post"]["poster"] is None


@pytest.mark.asyncio
async def test_post_poster_resolves_to_null_if_poster_is_deleted(
    query_public_api, post
):
    result = await query_public_api(POST_POSTER_QUERY, {"post": str(post.id)})
    assert result["data"]["post"]["poster"] is None


POST_THREAD_QUERY = """
    query GetPostThread($post: ID!) {
        post(id: $post) {
            id
            thread {
                id
                title
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_post_thread_is_resolved(query_public_api, post, thread):
    result = await query_public_api(POST_THREAD_QUERY, {"post": str(post.id)})
    assert result["data"]["post"]["thread"] == {
        "id": str(thread.id),
        "title": thread.title,
    }


POST_CATEGORY_QUERY = """
    query GetPostCategory($post: ID!) {
        post(id: $post) {
            id
            category {
                id
                name
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_post_category_is_resolved(query_public_api, category, post):
    result = await query_public_api(POST_CATEGORY_QUERY, {"post": str(post.id)})
    assert result["data"]["post"]["category"] == {
        "id": str(category.id),
        "name": category.name,
    }


POST_BODY_QUERY = """
    query GetPostBody($post: ID!) {
        post(id: $post) {
            id
            html
            richText
        }
    }
"""


@pytest.mark.asyncio
async def test_post_html_is_resolved(query_public_api, post):
    await post.update(rich_text=[{"id": "t3st", "type": "p", "text": "Hello world!"}])

    result = await query_public_api(POST_BODY_QUERY, {"post": str(post.id)})
    assert result["data"]["post"]["html"] == "<p>Hello world!</p>"


@pytest.mark.asyncio
async def test_post_rich_text_is_resolved(query_public_api, post):
    rich_text = [{"id": "t3st", "text": "Hello world!", "type": "p"}]
    await post.update(rich_text=rich_text)

    result = await query_public_api(POST_BODY_QUERY, {"post": str(post.id)})
    assert result["data"]["post"]["richText"] == rich_text


POST_URL_QUERY = """
    query GetPostUrl($post: ID!) {
        post(id: $post) {
            id
            url
            absoluteUrl: url(absolute: true)
        }
    }
"""


@pytest.mark.asyncio
async def test_post_url_resolves_to_posts_relative_url(query_public_api, thread, post):
    result = await query_public_api(POST_URL_QUERY, {"post": str(post.id)})
    assert result["data"]["post"]["url"] == (
        f"/t/{thread.slug}/{thread.id}/#post-{post.id}"
    )


@pytest.mark.asyncio
async def test_post_url_resolves_to_posts_absolute_url(query_public_api, thread, post):
    result = await query_public_api(POST_URL_QUERY, {"post": str(post.id)})
    assert result["data"]["post"]["absoluteUrl"] == (
        f"http://example.com/t/{thread.slug}/{thread.id}/#post-{post.id}"
    )


POST_EXTRA_QUERY = """
    query GetPostUrl($post: ID!) {
        post(id: $post) {
            id
            extra
        }
    }
"""


@pytest.mark.asyncio
async def test_post_extra_resolves_to_dict(query_public_api, post):
    result = await query_public_api(POST_EXTRA_QUERY, {"post": str(post.id)})
    assert result["data"]["post"]["extra"] == {}
