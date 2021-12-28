import pytest

from ...asgi import app
from ...testing import assert_contains


@pytest.mark.asyncio
async def test_thread_route_returns_response(http_client, thread):
    async with http_client as client:
        url = app.url_path_for("thread", slug=thread.slug, id=thread.id)
        response = await client.get(url)

    assert_contains(response, thread.title)


@pytest.mark.asyncio
async def test_thread_route_returns_301_for_invalid_slug(http_client, thread):
    async with http_client as client:
        url = app.url_path_for("thread", slug="outdated-slug", id=thread.id)
        response = await client.get(url)

    assert response.status_code == 301

    valid_url = app.url_path_for("thread", slug=thread.slug, id=thread.id)
    assert response.headers["location"].endswith(valid_url)


@pytest.mark.asyncio
async def test_thread_route_returns_301_for_invalid_slug_and_page(http_client, thread):
    async with http_client as client:
        url = app.url_path_for("thread", slug="outdated-slug", id=thread.id, page=1)
        response = await client.get(url)

    assert response.status_code == 301

    valid_url = app.url_path_for("thread", slug=thread.slug, id=thread.id)
    assert response.headers["location"].endswith(valid_url)


@pytest.mark.asyncio
async def test_thread_route_returns_301_for_explicit_first_page(http_client, thread):
    async with http_client as client:
        url = app.url_path_for("thread", slug=thread.slug, id=thread.id, page=1)
        response = await client.get(url)

    assert response.status_code == 301

    valid_url = app.url_path_for("thread", slug=thread.slug, id=thread.id)
    assert response.headers["location"].endswith(valid_url)


@pytest.mark.asyncio
async def test_thread_route_returns_404_for_non_existing_thread(db, http_client):
    async with http_client as client:
        url = app.url_path_for("thread", slug="slug", id=123)
        response = await client.get(url)

    assert response.status_code == 404
