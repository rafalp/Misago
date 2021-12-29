import pytest

from ...asgi import app
from ...testing import assert_contains, override_dynamic_settings


@pytest.mark.asyncio
@override_dynamic_settings(forum_index_threads=False)
async def test_index_route_returns_categories_list(http_client, category):
    async with http_client as client:
        url = app.url_path_for("index")
        response = await client.get(url)

    assert_contains(response, category.name)

    category_url = app.url_path_for("category", slug=category.slug, id=category.id)
    assert_contains(response, category_url)


@pytest.mark.asyncio
@override_dynamic_settings(forum_index_threads=True)
async def test_index_route_returns_threads_list(http_client, thread):
    async with http_client as client:
        url = app.url_path_for("index")
        response = await client.get(url)

    assert_contains(response, thread.title)

    thread_url = app.url_path_for("thread", slug=thread.slug, id=thread.id)
    assert_contains(response, thread_url)
