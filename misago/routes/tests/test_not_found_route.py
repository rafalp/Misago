import pytest


@pytest.mark.asyncio
async def test_not_found_route_renders_response(http_client, db):
    async with http_client() as client:
        response = await client.get("/not-found/")

    assert response.status_code == 404
