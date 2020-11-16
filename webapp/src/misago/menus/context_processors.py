from .menuitems import get_footer_menu_items, get_navbar_menu_items


def menus(request):
    return {
        "navbar_menu": get_navbar_menu_items(request.cache_versions),
        "footer_menu": get_footer_menu_items(request.cache_versions),
    }
