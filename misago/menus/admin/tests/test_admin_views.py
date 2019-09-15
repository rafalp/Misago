import pytest
from django.urls import reverse

from ....test import assert_contains
from ...models import MenuItem


def test_nav_contains_menus_item(admin_client, list_url):
    response = admin_client.get(list_url)
    assert_contains(response, reverse("misago:admin:settings:items:index"))


def test_empty_list_renders(admin_client, list_url):
    response = admin_client.get(list_url)
    assert response.status_code == 200


def test_list_renders_menu_item(admin_client, list_url, menu_item):
    response = admin_client.get(list_url)
    assert_contains(response, menu_item.title)


def test_menu_items_can_be_mass_deleted(admin_client, list_url, superuser):
    items = []
    for _ in range(10):
        item = MenuItem.objects.create(
            menu=MenuItem.POSITION_FOOTER,
            title="Test Item {}".format(_),
            item="https://items{}.com".format(_),
        )
        items.append(item.pk)

    assert MenuItem.objects.count() == 10

    response = admin_client.post(
        list_url, data={"action": "delete", "selected_items": items}
    )
    assert response.status_code == 302
    assert MenuItem.objects.count() == 0


def test_creation_form_renders(admin_client):
    response = admin_client.get(reverse("misago:admin:settings:items:new"))
    assert response.status_code == 200


def test_form_creates_new_menu_item(admin_client):
    response = admin_client.post(
        reverse("misago:admin:settings:items:new"),
        {
            "menu": MenuItem.POSITION_FOOTER,
            "title": "Test Item",
            "item": "https://admin.com/items/",
        },
    )

    item = MenuItem.objects.get()
    assert item.menu == MenuItem.POSITION_FOOTER
    assert item.title == "Test Item"
    assert item.item == "https://admin.com/items/"


def test_edit_form_renders(admin_client, menu_item):
    response = admin_client.get(
        reverse("misago:admin:settings:items:edit", kwargs={"pk": menu_item.pk})
    )
    assert_contains(response, menu_item.title)


def test_edit_form_updates_menu_items(admin_client, menu_item):
    response = admin_client.post(
        reverse("misago:admin:settings:items:edit", kwargs={"pk": menu_item.pk}),
        data={
            "menu": menu_item.POSITION_BOTH,
            "title": "Test Edited",
            "item": "https://example.com/edited/",
        },
    )
    assert response.status_code == 302

    menu_item.refresh_from_db()
    assert menu_item.menu == MenuItem.POSITION_BOTH
    assert menu_item.title == "Test Edited"
    assert menu_item.item == "https://example.com/edited/"


def test_menu_item_can_be_deleted(admin_client, menu_item):
    response = admin_client.post(
        reverse("misago:admin:settings:items:delete", kwargs={"pk": menu_item.pk})
    )
    assert response.status_code == 302

    with pytest.raises(MenuItem.DoesNotExist):
        menu_item.refresh_from_db()
