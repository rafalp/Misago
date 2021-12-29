import pytest

from ...asgi import app
from ...testing import assert_contains, assert_not_contains, override_dynamic_settings


@pytest.mark.asyncio
@override_dynamic_settings(forum_index_threads=False)
async def test_threads_route_returns_all_threads_list(
    http_client, thread, closed_category_thread
):
    async with http_client as client:
        url = app.url_path_for("threads")
        response = await client.get(url)

    assert_contains(response, thread.title)
    assert_contains(response, closed_category_thread.title)

    thread_url = app.url_path_for("thread", slug=thread.slug, id=thread.id)
    assert_contains(response, thread_url)

    other_thread_url = app.url_path_for(
        "thread",
        slug=closed_category_thread.slug,
        id=closed_category_thread.id,
    )
    assert_contains(response, other_thread_url)


@pytest.mark.asyncio
@override_dynamic_settings(forum_index_threads=False)
async def test_threads_route_slices_threads_list_by_cursor(
    http_client, thread, user_thread
):
    cursor = max([thread.last_post_id, user_thread.last_post_id])
    async with http_client as client:
        url = app.url_path_for("threads")
        url += f"?cursor={cursor}"
        response = await client.get(url)

    if cursor == thread.last_post_id:
        thread_url = app.url_path_for("thread", slug=thread.slug, id=thread.id)
        assert_not_contains(response, thread_url)
    else:
        thread_url = app.url_path_for(
            "thread",
            slug=user_thread.slug,
            id=user_thread.id,
        )
        assert_not_contains(response, thread_url)


@pytest.mark.asyncio
@override_dynamic_settings(forum_index_threads=False)
async def test_threads_route_returns_404_for_invalid_cursor(http_client, category):
    async with http_client as client:
        url = app.url_path_for("threads")
        url += f"?cursor=invalid"
        response = await client.get(url)

    assert response.status_code == 404


@pytest.mark.asyncio
@override_dynamic_settings(forum_index_threads=True)
async def test_threads_route_returns_404_if_threads_are_on_index(http_client, db):
    async with http_client as client:
        url = app.url_path_for("threads")
        response = await client.get(url)
        assert response.status_code == 404
