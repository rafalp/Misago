from unittest.mock import Mock

import pytest

from ..context import get_graphql_context


@pytest.mark.asyncio
async def test_graphql_context_includes_cache_versions(db):
    context = await get_graphql_context(None, {})
    assert context["cache_versions"]


@pytest.mark.asyncio
async def test_graphql_context_includes_settings_versions(db, dynamic_settings):
    context = await get_graphql_context(None, {})
    assert context["settings"] == dynamic_settings


@pytest.mark.asyncio
async def test_graphql_context_includes_preset_keys(db):
    context = await get_graphql_context(None, {"preset": True})
    assert context["preset"]


@pytest.mark.asyncio
async def test_graphql_context_includes_request(db):
    request = Mock()
    context = await get_graphql_context(request, {})
    assert context["request"] is request
