from .cache import set_menus_cache, get_menus_cache
from .models import MenuItem


def get_navbar_menu_items(cache_versions):
    return get_items(cache_versions).get(MenuItem.MENU_NAVBAR)


def get_footer_menu_items(cache_versions):
    return get_items(cache_versions).get(MenuItem.MENU_FOOTER)


def get_items(cache_versions):
    items = get_menus_cache(cache_versions)
    if items is None:
        items = get_items_from_db()
        set_menus_cache(cache_versions, items)
    return items


def get_items_from_db():
    return {
        MenuItem.MENU_NAVBAR: get_navbar_menu_items_from_db(),
        MenuItem.MENU_FOOTER: get_footer_menu_items_from_db(),
    }


def get_navbar_menu_items_from_db():
    return MenuItem.objects.exclude(menu=MenuItem.MENU_FOOTER).values()


def get_footer_menu_items_from_db():
    return MenuItem.objects.exclude(menu=MenuItem.MENU_NAVBAR).values()
