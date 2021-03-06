import pytest

from ..render import render, render_to_string

TEST_TEMPLATE = "__test__.html"


@pytest.mark.asyncio
async def test_template_is_rendered_to_string():
    html = await render_to_string(TEST_TEMPLATE)
    assert html == "TEST TEMPLATE"


@pytest.mark.asyncio
async def test_template_is_rendered_to_string_with_context():
    html = await render_to_string(TEST_TEMPLATE, {"value": "TEST CONTEXT"})
    assert html == "TEST CONTEXT"


@pytest.mark.asyncio
async def test_template_is_rendered_to_response(request_mock):
    response = await render(request_mock, TEST_TEMPLATE)
    assert response.body.decode(response.charset) == "TEST TEMPLATE"


@pytest.mark.asyncio
async def test_template_is_rendered_to_response_with_context(request_mock):
    response = await render(request_mock, TEST_TEMPLATE, {"value": "TEST CONTEXT"})
    assert response.body.decode(response.charset) == "TEST CONTEXT"


@pytest.mark.asyncio
async def test_template_is_rendered_to_response_with_default_status_code(request_mock):
    response = await render(request_mock, TEST_TEMPLATE)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_template_is_rendered_to_response_with_custom_status_code(request_mock):
    response = await render(request_mock, TEST_TEMPLATE, status_code=404)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_template_is_rendered_to_response_with_default_content_type(request_mock):
    response = await render(request_mock, TEST_TEMPLATE)
    assert response.media_type == "text/html"


@pytest.mark.asyncio
async def test_template_is_rendered_to_response_with_custom_content_type(request_mock):
    response = await render(request_mock, TEST_TEMPLATE, media_type="text/plain")
    assert response.media_type == "text/plain"
