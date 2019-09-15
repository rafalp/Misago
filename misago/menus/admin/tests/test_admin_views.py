import pytest
from django.urls import reverse

from ....test import assert_contains
from ...models import MenuLink


def test_nav_contains_menus_link(admin_client, list_url):
    response = admin_client.get(list_url)
    assert_contains(response, reverse("misago:admin:settings:links:index"))


def test_empty_list_renders(admin_client, list_url):
    response = admin_client.get(list_url)
    assert response.status_code == 200


def test_list_renders_menu_link(admin_client, list_url, menu_link):
    response = admin_client.get(list_url)
    assert_contains(response, menu_link.title)


def test_menu_links_can_be_mass_deleted(admin_client, list_url, superuser):
    links = []
    for _ in range(10):
        link = MenuLink.objects.create(
            position=MenuLink.POSITION_FOOTER,
            title="Test Link {}".format(_),
            link="https://links{}.com".format(_),
        )
        links.append(link.pk)

    assert MenuLink.objects.count() == 10

    response = admin_client.post(
        list_url, data={"action": "delete", "selected_items": links}
    )
    assert response.status_code == 302
    assert MenuLink.objects.count() == 0


def test_creation_form_renders(admin_client):
    response = admin_client.get(reverse("misago:admin:settings:links:new"))
    assert response.status_code == 200


def test_form_creates_new_menu_link(admin_client):
    response = admin_client.post(
        reverse("misago:admin:settings:links:new"),
        {
            "position": MenuLink.POSITION_FOOTER,
            "title": "Test Link",
            "link": "https://admin.com/links/",
        },
    )

    link = MenuLink.objects.get()
    assert link.position == MenuLink.POSITION_FOOTER
    assert link.title == "Test Link"
    assert link.link == "https://admin.com/links/"


def test_edit_form_renders(admin_client, menu_link):
    response = admin_client.get(
        reverse("misago:admin:settings:links:edit", kwargs={"pk": menu_link.pk})
    )
    assert_contains(response, menu_link.title)


def test_edit_form_updates_menu_links(admin_client, menu_link):
    response = admin_client.post(
        reverse("misago:admin:settings:links:edit", kwargs={"pk": menu_link.pk}),
        data={
            "position": menu_link.POSITION_BOTH,
            "title": "Test Edited",
            "link": "https://example.com/edited/",
        },
    )
    assert response.status_code == 302

    menu_link.refresh_from_db()
    assert menu_link.position == MenuLink.POSITION_BOTH
    assert menu_link.title == "Test Edited"
    assert menu_link.link == "https://example.com/edited/"


def test_menu_link_can_be_deleted(admin_client, menu_link):
    response = admin_client.post(
        reverse("misago:admin:settings:links:delete", kwargs={"pk": menu_link.pk})
    )
    assert response.status_code == 302

    with pytest.raises(MenuLink.DoesNotExist):
        menu_link.refresh_from_db()
