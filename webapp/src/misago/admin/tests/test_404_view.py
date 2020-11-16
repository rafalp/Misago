from django.urls import reverse

from ...test import assert_contains


def test_admin_displays_own_error_page_on_404_error(admin_client):
    response = admin_client.get(reverse("misago:admin:index") + "404-not-found/")
    assert_contains(response, "Administration", 404)
    assert_contains(response, "Requested page could not be found", 404)
