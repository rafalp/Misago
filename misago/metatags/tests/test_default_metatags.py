from django.conf import settings

from ...conf.dynamicsettings import DynamicSettings
from ...conf.models import Setting
from ..metatags import get_default_metatags


def test_get_default_metatags_returns_default_metatags_with_default_og_image(
    rf, dynamic_settings
):
    request = rf.get("/")
    request.settings = dynamic_settings

    metatags = {
        key: value.get_attrs() for key, value in get_default_metatags(request).items()
    }

    assert metatags == {
        "og:site_name": {
            "property": "og:site_name",
            "content": dynamic_settings.forum_name,
        },
        "og:type": {
            "property": "og:type",
            "content": "website",
        },
        "twitter:card": {
            "name": "twitter:card",
            "content": "summary",
        },
        "image": {
            "property": "og:image",
            "name": "twitter:image",
            "content": f"http://testserver/static/{settings.MISAGO_DEFAULT_OG_IMAGE}",
        },
        "image:width": {
            "property": "og:image:width",
            "content": str(settings.MISAGO_DEFAULT_OG_IMAGE_WIDTH),
        },
        "image:height": {
            "property": "og:image:height",
            "content": str(settings.MISAGO_DEFAULT_OG_IMAGE_HEIGHT),
        },
    }


def test_get_default_metatags_returns_default_metatags_with_custom_og_image(
    db, rf, cache_versions
):
    Setting.objects.filter(setting="og_image").update(
        image="custom-image.jpg", image_width=600, image_height=300
    )

    request = rf.get("/")
    request.settings = DynamicSettings(cache_versions)

    metatags = {
        key: value.get_attrs() for key, value in get_default_metatags(request).items()
    }

    assert metatags == {
        "og:site_name": {
            "property": "og:site_name",
            "content": request.settings.forum_name,
        },
        "og:type": {
            "property": "og:type",
            "content": "website",
        },
        "twitter:card": {
            "name": "twitter:card",
            "content": "summary",
        },
        "image": {
            "property": "og:image",
            "name": "twitter:image",
            "content": "http://testserver/media/custom-image.jpg",
        },
        "image:width": {
            "property": "og:image:width",
            "content": "600",
        },
        "image:height": {
            "property": "og:image:height",
            "content": "300",
        },
    }
