import pytest

from ...asgi import app
from ...testing import assert_contains


@pytest.mark.asyncio
async def test_admin_route_renders_admin_dashboard(db, http_client):
    async with http_client() as client:
        url = app.url_path_for("admin")
        response = await client.get(url)

    assert_contains(response, "admin")


@pytest.mark.asyncio
async def test_admin_route_is_catch_all(db, http_client):
    async with http_client() as client:
        url = app.url_path_for("admin")
        response = await client.get(f"{url}settings/some")

    assert_contains(response, "admin")
