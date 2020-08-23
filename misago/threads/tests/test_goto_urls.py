import pytest

from ..create import create_post
from ..goto import get_thread_last_post_url, get_thread_post_page, get_thread_post_url


@pytest.mark.asyncio
async def test_url_to_thread_last_post_is_returned(
    dynamic_settings, thread_with_reply, thread_reply
):
    thread = thread_with_reply

    url = await get_thread_last_post_url(dynamic_settings, thread)
    assert url == f"/t/{thread.slug}/{thread.id}/#post-{thread_reply.id}"


@pytest.mark.asyncio
async def test_url_to_thread_post_is_returned(
    dynamic_settings, thread_with_reply, thread_reply
):
    thread = thread_with_reply

    url = await get_thread_post_url(dynamic_settings, thread, thread_reply)
    assert url == f"/t/{thread.slug}/{thread.id}/#post-{thread_reply.id}"


@pytest.mark.asyncio
async def test_url_to_thread_first_post_is_returned(dynamic_settings, thread, post):
    url = await get_thread_post_url(dynamic_settings, thread, post)
    assert url == f"/t/{thread.slug}/{thread.id}/#post-{post.id}"


@pytest.mark.asyncio
async def test_thread_post_page_for_last_post_on_first_page_is_calculated_to_2(
    dynamic_settings, thread
):
    dynamic_settings["posts_per_page"] = 4
    dynamic_settings["posts_per_page_orphans"] = 0

    # fill in first page
    for _ in range(3):
        post = await create_post(thread, {}, poster_name="hello")
    # fill in next page
    for _ in range(dynamic_settings["posts_per_page"]):
        await create_post(thread, {}, poster_name="hello")

    page = await get_thread_post_page(dynamic_settings, thread, post)
    assert page == 2


@pytest.mark.asyncio
async def test_thread_post_page_for_last_post_on_first_page_is_calculated_to_1(
    dynamic_settings, thread
):
    dynamic_settings["posts_per_page"] = 4
    dynamic_settings["posts_per_page_orphans"] = 3

    # fill in first page
    for _ in range(3):
        post = await create_post(thread, {}, poster_name="hello")
    # fill in next page
    for _ in range(3):
        await create_post(thread, {}, poster_name="hello")

    page = await get_thread_post_page(dynamic_settings, thread, post)
    assert page == 1
