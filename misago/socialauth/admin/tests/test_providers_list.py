from django.urls import reverse


admin_link = reverse("misago:admin:settings:socialauth:index")


def test_providers_list_renders(admin_client):
    response = admin_client.get(admin_link)
    assert response.status_code == 200


def test_providers_list_renders_with_active_provider(admin_client, provider):
    response = admin_client.get(admin_link)
    assert response.status_code == 200


def test_providers_list_renders_with_disabled_provider(admin_client, disabled_provider):
    response = admin_client.get(admin_link)
    assert response.status_code == 200
