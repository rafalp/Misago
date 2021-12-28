import pytest

from ...asgi import app
from ...testing import assert_contains, assert_not_contains


@pytest.mark.asyncio
async def test_category_route_returns_response(http_client, category):
    async with http_client as client:
        url = app.url_path_for("category", slug=category.slug, id=category.id)
        response = await client.get(url)

    assert_contains(response, category.name)


@pytest.mark.asyncio
async def test_category_route_returns_category_threads_list(
    http_client, category, thread, closed_category_thread
):
    async with http_client as client:
        url = app.url_path_for("category", slug=category.slug, id=category.id)
        response = await client.get(url)

    assert_contains(response, thread.title)
    assert_not_contains(response, closed_category_thread.title)

    thread_url = app.url_path_for("thread", slug=thread.slug, id=thread.id)
    assert_contains(response, thread_url)

    other_category_thread_url = app.url_path_for(
        "thread",
        slug=closed_category_thread.slug,
        id=closed_category_thread.id,
    )
    assert_not_contains(response, other_category_thread_url)


@pytest.mark.asyncio
async def test_category_route_slices_threads_list_by_cursor(
    http_client, category, thread, user_thread
):
    cursor = max([thread.last_post_id, user_thread.last_post_id])
    async with http_client as client:
        url = app.url_path_for("category", slug=category.slug, id=category.id)
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
async def test_category_route_returns_301_for_invalid_slug(http_client, category):
    async with http_client as client:
        url = app.url_path_for("category", slug="outdated-slug", id=category.id)
        response = await client.get(url)

    assert response.status_code == 301

    valid_url = app.url_path_for("category", slug=category.slug, id=category.id)
    assert response.headers["location"].endswith(valid_url)


@pytest.mark.asyncio
async def test_category_route_returns_404_for_non_existing_category(db, http_client):
    async with http_client as client:
        url = app.url_path_for("category", slug="slug", id=123)
        response = await client.get(url)

    assert response.status_code == 404
