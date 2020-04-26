from unittest.mock import Mock

import pytest

from ..context import get_graphql_context


@pytest.fixture
def request_mock():
    return Mock(
        scope={"type": "request"}, state=Mock(cache_versions=Mock(), settings=Mock()),
    )


@pytest.mark.asyncio
async def test_graphql_context_includes_request(request_mock):
    context = await get_graphql_context(request_mock)
    assert context["request"] is request_mock


@pytest.mark.asyncio
async def test_graphql_context_includes_cache_versions(request_mock):
    context = await get_graphql_context(request_mock)
    assert context["cache_versions"] == request_mock.state.cache_versions


@pytest.mark.asyncio
async def test_graphql_context_includes_settings(request_mock):
    context = await get_graphql_context(request_mock)
    assert context["settings"] == request_mock.state.settings


@pytest.fixture
def websocket_mock():
    return Mock(scope={"type": "request"})


@pytest.mark.asyncio
async def test_graphql_websocket_context_includes_request(websocket_mock):
    context = await get_graphql_context(websocket_mock)
    assert context["request"] is websocket_mock


@pytest.mark.asyncio
async def test_graphql_websocket_context_includes_cache_versions(websocket_mock):
    context = await get_graphql_context(websocket_mock)
    assert context["cache_versions"]


@pytest.mark.asyncio
async def test_graphql_websocket_context_includes_settings(websocket_mock):
    context = await get_graphql_context(websocket_mock)
    assert context["settings"]
