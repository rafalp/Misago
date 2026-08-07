from django.conf import settings

from ...conf.test import override_dynamic_settings
from ..forumindex import get_forum_index_metatags


@override_dynamic_settings(index_title="Index Title")
def test_get_forum_index_metatags_includes_index_title_if_set(rf, dynamic_settings):
    request = rf.get("/")
    request.settings = dynamic_settings

    metatags = {
        key: value.get_attrs()
        for key, value in get_forum_index_metatags(request).items()
    }

    assert metatags == {
        "title": {
            "name": "twitter:title",
            "property": "og:title",
            "content": "Index Title",
        },
    }


@override_dynamic_settings(index_meta_description="Meta Description")
def test_get_forum_index_metatags_includes_index_meta_description_if_set(
    rf, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings

    metatags = {
        key: value.get_attrs()
        for key, value in get_forum_index_metatags(request).items()
    }

    assert metatags == {
        "description": {
            "name": "twitter:description",
            "property": "og:description",
            "content": "Meta Description",
        },
    }


@override_dynamic_settings(forum_address="http://example.com")
def test_get_forum_index_metatags_includes_forum_address_if_set(rf, dynamic_settings):
    request = rf.get("/")
    request.settings = dynamic_settings

    metatags = {
        key: value.get_attrs()
        for key, value in get_forum_index_metatags(request).items()
    }

    assert metatags == {
        "url": {
            "name": "twitter:url",
            "property": "og:url",
            "content": "http://example.com",
        },
    }
