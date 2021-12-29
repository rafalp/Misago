from unittest.mock import Mock

import pytest

from ..exceptions import server_error_route


@pytest.mark.asyncio
async def test_server_error_route_renders_response():
    response = await server_error_route(Mock(), ValueError("Test Error"))
    assert response.status_code == 500
    assert str(response.body)
