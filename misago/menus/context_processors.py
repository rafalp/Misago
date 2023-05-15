from typing import List

from .menuitems import get_footer_menu_items, get_navbar_menu_items
from .models import MenuItem


def menus(request):
    navbar_items = get_navbar_menu_items(request.cache_versions)
    footer_items = get_footer_menu_items(request.cache_versions)

    navbarItemsJson = serialize_items(navbar_items)
    footerItemsJson = []

    navbarUrls = [item["url"] for item in navbarItemsJson]
    for footerItem in serialize_items(footer_items):
        if footerItem["url"] not in navbarUrls:
            footerItemsJson.append(footerItem)

    request.frontend_context.update(
        {
            "extraMenuItems": navbarItemsJson,
            "extraFooterItems": footerItemsJson,
        }
    )

    return {
        "navbar_menu": navbar_items,
        "footer_menu": footer_items,
    }


def serialize_items(items: List[MenuItem]) -> List[dict]:
    serialized = []
    for item in items:
        serialized.append(
            {
                "title": item["title"],
                "url": item["url"],
                "className": item["css_class"],
                "targetBlank": item["target_blank"],
                "rel": item["rel"],
            }
        )
    return serialized
