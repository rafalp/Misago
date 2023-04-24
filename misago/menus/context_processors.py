from typing import List

from .menuitems import get_footer_menu_items, get_navbar_menu_items
from .models import MenuItem


def menus(request):
    navbar_items = get_navbar_menu_items(request.cache_versions)

    request.frontend_context.update({
        "extraMenuItems": serialize_items(navbar_items)
    })

    return {
        "navbar_menu": navbar_items,
        "footer_menu": get_footer_menu_items(request.cache_versions),
    }


def serialize_items(items: List[MenuItem]) -> List[dict]:
    serialized = []
    for item in items:
        serialized.append({
            "title": item["title"],
            "url": item["url"],
            "className": item["css_class"],
            "targetBlank": item["target_blank"],
            "rel": item["rel"],
        })
    return serialized