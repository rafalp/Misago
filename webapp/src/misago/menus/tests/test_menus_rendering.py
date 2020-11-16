from django.urls import reverse

from ...test import assert_contains


def test_custom_menu_items_are_rendered_in_navbar(client, navar_menu_item):
    response = client.get(reverse("misago:index"))
    assert_contains(response, navar_menu_item.url)


def test_custom_menu_items_are_rendered_in_footer(client, footer_menu_item):
    response = client.get(reverse("misago:index"))
    assert_contains(response, footer_menu_item.url)


def test_custom_menu_items_are_rendered_in_both_menus(client, both_menus_item):
    response = client.get(reverse("misago:index"))
    assert_contains(response, both_menus_item.url)
