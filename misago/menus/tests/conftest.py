import pytest

from ..menuitems import get_footer_menu_items, get_navbar_menu_items
from ..models import MenuItem


@pytest.fixture
def navar_menu_item(db):
    return MenuItem.objects.create(
        title="Top Menu Item",
        url="https://navbar_menu_item.com",
        menu=MenuItem.MENU_NAVBAR,
    )


@pytest.fixture
def footer_menu_item(db):
    return MenuItem.objects.create(
        title="Footer Menu Item",
        url="https://footer_menu_item.com",
        menu=MenuItem.MENU_FOOTER,
    )


@pytest.fixture
def both_menus_item(db):
    return MenuItem.objects.create(
        title="Both Positions Menu Item",
        url="https://both_menus_menu_item.com",
        menu=MenuItem.MENU_BOTH,
    )


@pytest.fixture
def menu_item_with_attributes(db):
    return MenuItem.objects.create(
        title="Menu item with attributes",
        url="https://menu_item_with_attributes.com",
        menu=MenuItem.MENU_BOTH,
        rel="noopener nofollow",
        target_blank=True,
        css_class="test-item-css-class",
    )


@pytest.fixture
def navbar_menu_items(
    db, cache_versions, navar_menu_item, both_menus_item, menu_item_with_attributes
):
    return get_navbar_menu_items(cache_versions)


@pytest.fixture
def footer_menu_items(
    db, cache_versions, footer_menu_item, both_menus_item, menu_item_with_attributes
):
    return get_footer_menu_items(cache_versions)
