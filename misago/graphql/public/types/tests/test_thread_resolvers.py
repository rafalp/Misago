import pytest

from .....users.update import update_user
from ..thread import (
    resolve_category,
    resolve_first_post,
    resolve_last_post,
    resolve_last_post_url,
    resolve_last_poster,
    resolve_post,
    resolve_post_url,
    resolve_posts,
    resolve_starter,
)


@pytest.mark.asyncio
async def test_category_resolver_returns_thread_category(
    graphql_info, category, thread
):
    value = await resolve_category(thread, graphql_info)
    assert value == category


@pytest.mark.asyncio
async def test_posts_resolver_returns_thread_posts_paginator(
    graphql_info, thread, post
):
    value = await resolve_posts(thread, graphql_info)
    assert value.get_count() == 1
    assert value.get_pages() == 1


@pytest.mark.asyncio
async def test_first_post_resolver_returns_threads_first_post(
    graphql_info, thread, post
):
    value = await resolve_first_post(thread, graphql_info)
    assert value == post


@pytest.mark.asyncio
async def test_last_post_resolver_returns_threads_last_post(graphql_info, thread, post):
    value = await resolve_last_post(thread, graphql_info)
    assert value == post


@pytest.mark.asyncio
async def test_starter_resolver_returns_thread_starter(graphql_info, user_thread, user):
    value = await resolve_starter(user_thread, graphql_info)
    assert value == user


@pytest.mark.asyncio
async def test_starter_resolver_returns_none_if_thread_starter_is_inactive(
    graphql_info, user_thread, user
):
    await update_user(user, is_active=False)
    value = await resolve_starter(user_thread, graphql_info)
    assert value is None


@pytest.mark.asyncio
async def test_starter_resolver_returns_none_if_starter_is_empty(graphql_info, thread):
    value = await resolve_starter(thread, graphql_info)
    assert value is None


@pytest.mark.asyncio
async def test_last_poster_resolver_returns_threads_last_poster(
    graphql_info, user_thread, user
):
    value = await resolve_last_poster(user_thread, graphql_info)
    assert value == user


@pytest.mark.asyncio
async def test_last_poster_resolver_returns_none_if_threads_last_poster_is_inactive(
    graphql_info, user_thread, user
):
    await update_user(user, is_active=False)
    value = await resolve_last_poster(user_thread, graphql_info)
    assert value is None


@pytest.mark.asyncio
async def test_last_poster_resolver_returns_none_if_last_poster_is_empty(
    graphql_info, thread
):
    value = await resolve_last_poster(thread, graphql_info)
    assert value is None


@pytest.mark.asyncio
async def test_post_resolver_returns_thread_post(graphql_info, thread, post):
    value = await resolve_post(thread, graphql_info, id=post.id)
    assert value == post


@pytest.mark.asyncio
async def test_post_resolver_returns_none_if_post_is_in_other_thread(
    graphql_info, thread, closed_thread_post
):
    value = await resolve_post(thread, graphql_info, id=closed_thread_post.id)
    assert value is None


@pytest.mark.asyncio
async def test_post_resolver_returns_none_if_post_doesnt_exist(
    graphql_info, thread, post
):
    value = await resolve_post(thread, graphql_info, id=post.id + 1)
    assert value is None


@pytest.mark.asyncio
async def test_last_post_url_resolver_returns_url_to_thread_last_post(
    graphql_info, thread, post
):
    value = await resolve_last_post_url(thread, graphql_info)
    assert value == f"/t/{thread.slug}/{thread.id}/#post-{post.id}"


@pytest.mark.asyncio
async def test_last_post_url_resolver_returns_absolute_url_to_thread_last_post(
    graphql_info, thread, post
):
    value = await resolve_last_post_url(thread, graphql_info, absolute=True)
    assert value == f"http://test.com/t/{thread.slug}/{thread.id}/#post-{post.id}"


@pytest.mark.asyncio
async def test_post_url_resolver_returns_url_to_specified_thread_post(
    graphql_info, thread, post
):
    value = await resolve_post_url(thread, graphql_info, id=post.id)
    assert value == f"/t/{thread.slug}/{thread.id}/#post-{post.id}"


@pytest.mark.asyncio
async def test_post_url_resolver_returns_absolute_url_to_specified_thread_post(
    graphql_info, thread, post
):
    value = await resolve_post_url(thread, graphql_info, id=post.id, absolute=True)
    assert value == f"http://test.com/t/{thread.slug}/{thread.id}/#post-{post.id}"


@pytest.mark.asyncio
async def test_post_url_resolver_returns_none_if_post_is_not_found(
    graphql_info, thread, post
):
    value = await resolve_post_url(thread, graphql_info, id=post.id * 10)
    assert value is None


@pytest.mark.asyncio
async def test_post_url_resolver_returns_none_if_post_belongs_to_other_thread(
    graphql_info, thread, post, closed_thread_post
):
    value = await resolve_post_url(thread, graphql_info, id=closed_thread_post.id)
    assert value is None
