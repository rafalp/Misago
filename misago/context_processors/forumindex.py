from django.http import HttpRequest

from ..forumindex.menus import get_main_menu_items
from ..menus.menu import BoundMenuItem


def main_menu(request: HttpRequest) -> dict:
    main_menu = get_main_menu_items(request)

    request.frontend_context.update(
        {"main_menu": list(map(serialize_menu_item, main_menu))}
    )

    return {
        "main_menu": main_menu,
        "main_menu_index": main_menu[0],
    }


def serialize_menu_item(item: BoundMenuItem) -> dict:
    return {
        "key": item.key,
        "url": item.url,
        "label": item.label,
    }
