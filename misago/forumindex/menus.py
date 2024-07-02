from dataclasses import replace

from django.http import HttpRequest
from django.urls import reverse
from django.utils.translation import pgettext_lazy

from ..menus.menu import BoundMenuItem, Menu


main_menu = Menu()

main_menu.add_item(
    key="threads",
    url_name="misago:threads",
    label=pgettext_lazy("main menu item", "Threads"),
)
main_menu.add_item(
    key="categories",
    url_name="misago:categories",
    label=pgettext_lazy("main menu item", "Categories"),
)


def get_main_menu_items(request: HttpRequest) -> list[BoundMenuItem]:
    menu = main_menu.bind_to_request(request)
    menu_items = {item.key: item for item in menu.items}

    final_menu: list[BoundMenuItem] = []

    if forum_index := menu_items.pop(request.settings.index_view, None):
        final_menu.append(replace(forum_index, url=reverse("misago:index")))

    final_menu += menu_items.values()

    return final_menu
