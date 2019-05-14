from django.urls import reverse


def test_general_settings_form_renders(admin_client):
    response = admin_client.get(reverse("misago:admin:settings:general:index"))
    assert response.status_code == 200
