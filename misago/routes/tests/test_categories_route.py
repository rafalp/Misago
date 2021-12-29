import pytest

from ...asgi import app
from ...testing import assert_contains, override_dynamic_settings


@pytest.mark.asyncio
@override_dynamic_settings(forum_index_threads=True)
async def test_categories_route_returns_categories_list(http_client, category):
    async with http_client as client:
        url = app.url_path_for("categories")
        response = await client.get(url)

    assert_contains(response, category.name)

    category_url = app.url_path_for("category", slug=category.slug, id=category.id)
    assert_contains(response, category_url)


@pytest.mark.asyncio
@override_dynamic_settings(forum_index_threads=False)
async def test_categories_route_returns_404_if_categories_are_on_index(http_client, db):
    async with http_client as client:
        url = app.url_path_for("categories")
        response = await client.get(url)
        assert response.status_code == 404
