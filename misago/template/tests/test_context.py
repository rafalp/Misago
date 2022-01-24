import pytest

from ..context import get_template_context


@pytest.mark.asyncio
async def test_final_template_context_is_created_from_request_mock(request_mock):
    context = await get_template_context(request_mock)
    assert context["request"] is request_mock
    assert context["cache_versions"] is request_mock.state.cache_versions
    assert context["settings"] is request_mock.state.settings


@pytest.mark.asyncio
async def test_final_template_context_includes_extra_context(request_mock):
    final_context = await get_template_context(request_mock, {"test": True})
    assert final_context["test"] is True


@pytest.mark.asyncio
async def test_final_template_context_merges_default_context_with_extra_context(
    request_mock,
):
    context = await get_template_context(request_mock, {"settings": True})
    assert context["request"] is request_mock
    assert context["cache_versions"] is request_mock.state.cache_versions
    assert context["settings"] is True
