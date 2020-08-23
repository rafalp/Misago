import pytest

from ..posts import (
    THREAD_POST_URL_CONTEXT_KEY,
    clear_all_posts_urls,
    clear_post_url,
    load_thread_post_url,
)


@pytest.mark.asyncio
async def test_thread_post_url_loader_returns_post_url(graphql_context, thread, post):
    post_url = await load_thread_post_url(graphql_context, thread, post)
    assert post_url == f"/t/{thread.slug}/{thread.id}/#post-{post.id}"


@pytest.mark.asyncio
async def test_thread_post_url_loader_clears_post_url(graphql_context, thread, post):
    await load_thread_post_url(graphql_context, thread, post)
    assert graphql_context[THREAD_POST_URL_CONTEXT_KEY][post.id]

    clear_post_url(graphql_context, post)
    assert post.id not in graphql_context[THREAD_POST_URL_CONTEXT_KEY]


@pytest.mark.asyncio
async def test_thread_post_url_loader_doesnt_error_when_nonexisting_post_is_cleared(
    graphql_context, post
):
    graphql_context[THREAD_POST_URL_CONTEXT_KEY] = {}
    clear_post_url(graphql_context, post)
    assert graphql_context[THREAD_POST_URL_CONTEXT_KEY] == {}


def test_clearings_post_url_cache_works_on_unitialized_context(post):
    context = {}
    clear_post_url(context, post)
    assert context == {}


@pytest.mark.asyncio
async def test_thread_post_url_loader_clears_all_posts_urls(
    graphql_context, thread, post
):
    await load_thread_post_url(graphql_context, thread, post)
    assert graphql_context[THREAD_POST_URL_CONTEXT_KEY][post.id]

    clear_all_posts_urls(graphql_context)
    assert graphql_context[THREAD_POST_URL_CONTEXT_KEY] == {}


@pytest.mark.asyncio
async def test_clearings_all_posts_urls_cache_works_on_unitialized_context():
    context = {}
    clear_all_posts_urls(context)
    assert context[THREAD_POST_URL_CONTEXT_KEY] == {}
