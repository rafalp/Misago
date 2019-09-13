from django.urls import reverse

from ....cache.test import assert_invalidates_cache
from ... import MENU_LINKS_CACHE


def test_top_menu_link_can_be_moved_down(admin_client, menu_link, other_menu_link):
    menu_link.order = 0
    menu_link.save()

    other_menu_link.order = 1
    other_menu_link.save()

    admin_client.post(
        reverse("misago:admin:settings:links:down", kwargs={"pk": menu_link.pk})
    )

    menu_link.refresh_from_db()
    assert menu_link.order == 1
    other_menu_link.refresh_from_db()
    assert other_menu_link.order == 0


def test_top_menu_link_cant_be_moved_up(admin_client, menu_link, other_menu_link):
    menu_link.order = 0
    menu_link.save()

    other_menu_link.order = 1
    other_menu_link.save()

    admin_client.post(
        reverse("misago:admin:settings:links:up", kwargs={"pk": menu_link.pk})
    )

    menu_link.refresh_from_db()
    assert menu_link.order == 0
    other_menu_link.refresh_from_db()
    assert other_menu_link.order == 1


def test_bottom_menu_link_cant_be_moved_down(admin_client, menu_link, other_menu_link):
    menu_link.order = 1
    menu_link.save()

    other_menu_link.order = 0
    other_menu_link.save()

    admin_client.post(
        reverse("misago:admin:settings:links:down", kwargs={"pk": menu_link.pk})
    )

    menu_link.refresh_from_db()
    assert menu_link.order == 1
    other_menu_link.refresh_from_db()
    assert other_menu_link.order == 0


def test_bottom_menu_link_can_be_moved_up(admin_client, menu_link, other_menu_link):
    menu_link.order = 1
    menu_link.save()

    other_menu_link.order = 0
    other_menu_link.save()

    admin_client.post(
        reverse("misago:admin:settings:links:up", kwargs={"pk": menu_link.pk})
    )

    menu_link.refresh_from_db()
    assert menu_link.order == 0
    other_menu_link.refresh_from_db()
    assert other_menu_link.order == 1


def test_moving_menu_link_down_invalidates_menu_links_cache(
    admin_client, menu_link, other_menu_link
):
    menu_link.order = 0
    menu_link.save()

    other_menu_link.order = 1
    other_menu_link.save()

    with assert_invalidates_cache(MENU_LINKS_CACHE):
        admin_client.post(
            reverse("misago:admin:settings:links:down", kwargs={"pk": menu_link.pk})
        )


def test_moving_menu_link_up_invalidates_menu_links_cache(
    admin_client, menu_link, other_menu_link
):
    menu_link.order = 1
    menu_link.save()

    other_menu_link.order = 0
    other_menu_link.save()

    with assert_invalidates_cache(MENU_LINKS_CACHE):
        admin_client.post(
            reverse("misago:admin:settings:links:up", kwargs={"pk": menu_link.pk})
        )
