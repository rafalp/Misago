from django.conf import settings as dj_settings
from django.http import HttpRequest
from django.templatetags.static import static

from .default import get_default_metatags
from .hooks import get_forum_index_metatags_hook
from .metatag import MetaTag


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
