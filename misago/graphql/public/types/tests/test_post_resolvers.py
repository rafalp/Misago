import pytest


POST_QUERY = """
    query GetPost($post: ID!) {
        post(id: $post) {
            id
            url
            absoluteUrl: url(absolute: true)
            html
            richText
            poster {
                id
                name
            }
            thread {
                id
                title
            }
            category {
                id
                name
            }
            extra
        }
    }
"""


@pytest.mark.asyncio
async def test_post_query_is_resolved_by_id(query_public_api, user_post):
    result = await query_public_api(POST_QUERY, {"post": str(user_post.id)})
    assert result["data"]["post"]["id"] == str(user_post.id)


@pytest.mark.asyncio
async def test_post_query_is_resolved_to_none_for_nonexisting_post(
    query_public_api, user_post
):
    result = await query_public_api(POST_QUERY, {"post": str(user_post.id * 1000)})
    assert result["data"]["post"] is None


@pytest.mark.asyncio
async def test_post_poster_is_resolved(query_public_api, user_post, user):
    result = await query_public_api(POST_QUERY, {"post": str(user_post.id)})
    assert result["data"]["post"]["poster"] == {
        "id": str(user.id),
        "name": user.name,
    }


@pytest.mark.asyncio
async def test_post_poster_is_resolved_to_null_if_user_is_inactive(
    query_public_api, user_post, user
):
    await user.update(is_active=False)

    result = await query_public_api(POST_QUERY, {"post": str(user_post.id)})
    assert result["data"]["post"]["poster"] is None


@pytest.mark.asyncio
async def test_post_poster_is_resolved_to_null_if_poster_is_deleted(
    query_public_api, post
):
    result = await query_public_api(POST_QUERY, {"post": str(post.id)})
    assert result["data"]["post"]["poster"] is None


@pytest.mark.asyncio
async def test_post_thread_is_resolved(query_public_api, post, thread):
    result = await query_public_api(POST_QUERY, {"post": str(post.id)})
    assert result["data"]["post"]["thread"] == {
        "id": str(thread.id),
        "title": thread.title,
    }


@pytest.mark.asyncio
async def test_post_category_is_resolved(query_public_api, category, post):
    result = await query_public_api(POST_QUERY, {"post": str(post.id)})
    assert result["data"]["post"]["category"] == {
        "id": str(category.id),
        "name": category.name,
    }


@pytest.mark.asyncio
async def test_post_html_is_resolved(query_public_api, post):
    await post.update(rich_text=[{"id": "t3st", "type": "p", "text": "Hello world!"}])

    result = await query_public_api(POST_QUERY, {"post": str(post.id)})
    assert result["data"]["post"]["html"] == "<p>Hello world!</p>"


@pytest.mark.asyncio
async def test_post_rich_text_is_resolved(query_public_api, post):
    rich_text = [{"id": "t3st", "text": "Hello world!", "type": "p"}]
    await post.update(rich_text=rich_text)

    result = await query_public_api(POST_QUERY, {"post": str(post.id)})
    assert result["data"]["post"]["richText"] == rich_text


@pytest.mark.asyncio
async def test_post_url_is_resolved_to_posts_relative_url(
    query_public_api, thread, post
):
    result = await query_public_api(POST_QUERY, {"post": str(post.id)})
    assert result["data"]["post"]["url"] == (
        f"/t/{thread.slug}/{thread.id}/#post-{post.id}"
    )


@pytest.mark.asyncio
async def test_post_url_is_resolved_to_posts_absolute_url(
    query_public_api, thread, post
):
    result = await query_public_api(POST_QUERY, {"post": str(post.id)})
    assert result["data"]["post"]["absoluteUrl"] == (
        f"http://example.com/t/{thread.slug}/{thread.id}/#post-{post.id}"
    )


@pytest.mark.asyncio
async def test_post_extra_is_resolved_to_dict(query_public_api, post):
    result = await query_public_api(POST_QUERY, {"post": str(post.id)})
    assert result["data"]["post"]["extra"] == {}
