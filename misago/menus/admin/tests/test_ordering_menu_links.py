from django.urls import reverse

from ....cache.test import assert_invalidates_cache
from ... import MENU_ITEMS_CACHE


def test_top_menu_item_can_be_moved_down(admin_client, menu_item, other_menu_item):
    menu_item.order = 0
    menu_item.save()

    other_menu_item.order = 1
    other_menu_item.save()

    admin_client.post(
        reverse("misago:admin:settings:menu-items:down", kwargs={"pk": menu_item.pk})
    )

    menu_item.refresh_from_db()
    assert menu_item.order == 1
    other_menu_item.refresh_from_db()
    assert other_menu_item.order == 0


def test_top_menu_item_cant_be_moved_up(admin_client, menu_item, other_menu_item):
    menu_item.order = 0
    menu_item.save()

    other_menu_item.order = 1
    other_menu_item.save()

    admin_client.post(
        reverse("misago:admin:settings:menu-items:up", kwargs={"pk": menu_item.pk})
    )

    menu_item.refresh_from_db()
    assert menu_item.order == 0
    other_menu_item.refresh_from_db()
    assert other_menu_item.order == 1


def test_bottom_menu_item_cant_be_moved_down(admin_client, menu_item, other_menu_item):
    menu_item.order = 1
    menu_item.save()

    other_menu_item.order = 0
    other_menu_item.save()

    admin_client.post(
        reverse("misago:admin:settings:menu-items:down", kwargs={"pk": menu_item.pk})
    )

    menu_item.refresh_from_db()
    assert menu_item.order == 1
    other_menu_item.refresh_from_db()
    assert other_menu_item.order == 0


def test_bottom_menu_item_can_be_moved_up(admin_client, menu_item, other_menu_item):
    menu_item.order = 1
    menu_item.save()

    other_menu_item.order = 0
    other_menu_item.save()

    admin_client.post(
        reverse("misago:admin:settings:menu-items:up", kwargs={"pk": menu_item.pk})
    )

    menu_item.refresh_from_db()
    assert menu_item.order == 0
    other_menu_item.refresh_from_db()
    assert other_menu_item.order == 1


def test_moving_menu_item_down_invalidates_menu_items_cache(
    admin_client, menu_item, other_menu_item
):
    menu_item.order = 0
    menu_item.save()

    other_menu_item.order = 1
    other_menu_item.save()

    with assert_invalidates_cache(MENU_ITEMS_CACHE):
        admin_client.post(
            reverse(
                "misago:admin:settings:menu-items:down", kwargs={"pk": menu_item.pk}
            )
        )


def test_moving_menu_item_up_invalidates_menu_items_cache(
    admin_client, menu_item, other_menu_item
):
    menu_item.order = 1
    menu_item.save()

    other_menu_item.order = 0
    other_menu_item.save()

    with assert_invalidates_cache(MENU_ITEMS_CACHE):
        admin_client.post(
            reverse("misago:admin:settings:menu-items:up", kwargs={"pk": menu_item.pk})
        )
