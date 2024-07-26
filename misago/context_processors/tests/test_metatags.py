from ...metatags.metatags import get_default_metatags
from ...test import assert_contains
from ..metatags import default_metatags


def test_default_metatags_context_processor_returns_default_metatags(
    rf, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings

    context = default_metatags(request)
    assert "og:site_name" in context["default_metatags"]


def test_default_metatags_are_rendered_in_response_html(rf, dynamic_settings, client):
    request = rf.get("/")
    request.settings = dynamic_settings
    default_metatags = get_default_metatags(request)

    response = client.get("/")
    for metatag in default_metatags.values():
        assert_contains(response, metatag.as_html())
