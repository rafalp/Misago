from django.urls import reverse


def test_form_displays_for_enabled_provider(admin_client, provider):
    response = admin_client.get(
        reverse("misago:admin:settings:socialauth:edit", kwargs={"pk": provider.pk})
    )
    assert response.status_code == 200


def test_form_displays_for_disabled_provider(admin_client, disabled_provider):
    response = admin_client.get(
        reverse(
            "misago:admin:settings:socialauth:edit", kwargs={"pk": disabled_provider.pk}
        )
    )
    assert response.status_code == 200


def test_form_displays_for_unset_provider(admin_client):
    response = admin_client.get(
        reverse("misago:admin:settings:socialauth:edit", kwargs={"pk": "facebook"})
    )
    assert response.status_code == 200


def test_form_handles_undefined_provider(admin_client):
    response = admin_client.get(
        reverse("misago:admin:settings:socialauth:edit", kwargs={"pk": "undefined"})
    )
    assert response.status_code == 302
