from django.urls import reverse

from ....test import assert_contains


def test_link_is_registered_in_admin_nav(admin_client):
    response = admin_client.get(reverse("misago:admin:index"))
    assert_contains(response, reverse("misago:admin:settings:index"))


def test_settings_grid_renders(admin_client):
    response = admin_client.get(reverse("misago:admin:settings:index"))
    assert response.status_code == 200
