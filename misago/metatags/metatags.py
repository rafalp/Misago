from django.conf import settings as dj_settings
from django.http import HttpRequest
from django.templatetags.static import static

from .hooks import get_default_metatags_hook, get_forum_index_metatags_hook
from .metatag import MetaTag

__all__ = ["MetaTag", "get_default_metatags", "get_forum_index_metatags"]


def get_default_metatags(request: HttpRequest) -> dict[str, MetaTag]:
    return get_default_metatags_hook(_get_default_metatags_action, request)


def _get_default_metatags_action(request: HttpRequest) -> dict[str, MetaTag]:
    settings = request.settings

    metatags = {
        "og:site_name": MetaTag(property="og:site_name", content=settings.forum_name),
        "og:type": MetaTag(property="og:type", content="website"),
        "twitter:card": MetaTag(name="twitter:card", content="summary"),
    }

    og_image = request.settings.get("og_image")
    if og_image["value"]:
        metatags.update(
            {
                "image": MetaTag(
                    property="og:image",
                    name="twitter:image",
                    content=request.build_absolute_uri(og_image["value"]),
                ),
                "image:width": MetaTag(
                    property="og:image:width", content=og_image["width"]
                ),
                "image:height": MetaTag(
                    property="og:image:height", content=og_image["height"]
                ),
            }
        )
    else:
        og_image_url = request.build_absolute_uri(
            static(dj_settings.MISAGO_DEFAULT_OG_IMAGE)
        )

        metatags.update(
            {
                "image": MetaTag(
                    property="og:image",
                    name="twitter:image",
                    content=og_image_url,
                ),
                "image:width": MetaTag(
                    property="og:image:width",
                    content=dj_settings.MISAGO_DEFAULT_OG_IMAGE_WIDTH,
                ),
                "image:height": MetaTag(
                    property="og:image:height",
                    content=dj_settings.MISAGO_DEFAULT_OG_IMAGE_HEIGHT,
                ),
            }
        )

    return metatags


def get_forum_index_metatags(request: HttpRequest) -> dict[str, MetaTag]:
    return get_forum_index_metatags_hook(_get_forum_index_metatags_action, request)


def _get_forum_index_metatags_action(request: HttpRequest) -> dict[str, MetaTag]:
    metatags = get_default_metatags(request)

    if request.settings.index_title:
        metatags["title"] = MetaTag(
            property="og:title",
            name="twitter:title",
            content=request.settings.index_title,
        )

    if request.settings.index_meta_description:
        metatags["description"] = MetaTag(
            property="og:description",
            name="twitter:description",
            content=request.settings.index_meta_description,
        )

    if request.settings.forum_address:
        metatags["url"] = MetaTag(
            property="og:url",
            name="twitter:url",
            content=request.settings.forum_address,
        )

    return metatags
