from unittest.mock import Mock

from ..menus import get_main_menu_items


def test_get_main_menu_items_returns_categories_as_first_item():
    main_menu = get_main_menu_items(
        Mock(path_info="/", settings=Mock(index_view="categories"))
    )

    assert main_menu[0].key == "categories"
    assert main_menu[1].key == "threads"


def test_get_main_menu_items_returns_threads_as_first_item():
    main_menu = get_main_menu_items(
        Mock(path_info="/", settings=Mock(index_view="threads"))
    )

    assert main_menu[0].key == "threads"
    assert main_menu[1].key == "categories"


def test_get_main_menu_items_returns_threads_as_first_item_if_setting_is_invalid():
    main_menu = get_main_menu_items(
        Mock(path_info="/", settings=Mock(index_view="invalid"))
    )

    assert main_menu[0].key == "threads"
    assert main_menu[1].key == "categories"
