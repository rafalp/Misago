from django.db.models import Q

from .cache import set_menus_cache, get_menus_cache
from .models import MenuLink


def get_top_menu_links(cache_versions):
    return get_links(cache_versions).get(MenuLink.POSITION_TOP)


def get_footer_menu_links(cache_versions):
    return get_links(cache_versions).get(MenuLink.POSITION_FOOTER)


def get_links(cache_versions):
    links = get_menus_cache(cache_versions)
    if links is None:
        links = get_links_from_db()
        set_menus_cache(cache_versions, links)
    return links


def get_links_from_db():
    links = {
        MenuLink.POSITION_TOP: _get_footer_menu_links_from_db(),
        MenuLink.POSITION_FOOTER: _get_top_menu_links_from_db(),
    }
    return links


def _get_footer_menu_links_from_db():
    return MenuLink.objects.filter(
        Q(position=MenuLink.POSITION_TOP) | Q(position=MenuLink.POSITION_BOTH)
    ).values()


def _get_top_menu_links_from_db():
    return MenuLink.objects.filter(
        Q(position=MenuLink.POSITION_FOOTER) | Q(position=MenuLink.POSITION_BOTH)
    ).values()









