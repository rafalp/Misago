from django.urls import reverse

from ....cache.test import assert_invalidates_cache
from ....test import assert_contains
from ... import SOCIALAUTH_CACHE
from ...models import SocialAuthProvider


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


def test_form_displays_provider_settings(admin_client, provider):
    provider.settings = {"key": "test-key", "secret": "test-secret"}
    provider.save()

    response = admin_client.get(
        reverse("misago:admin:settings:socialauth:edit", kwargs={"pk": provider.pk})
    )

    assert_contains(response, "test-key")
    assert_contains(response, "test-secret")


def test_form_updates_provider_settings(admin_client, provider):
    admin_client.post(
        reverse("misago:admin:settings:socialauth:edit", kwargs={"pk": provider.pk}),
        {"key": "test-key", "secret": "test-secret"},
    )

    provider.refresh_from_db()
    assert provider.settings == {
        "associate_by_email": 0,
        "key": "test-key",
        "secret": "test-secret",
    }


def test_form_updates_provider_button_text(admin_client, provider):
    admin_client.post(
        reverse("misago:admin:settings:socialauth:edit", kwargs={"pk": provider.pk}),
        {"button_text": "Hello world!"},
    )

    provider.refresh_from_db()
    assert provider.button_text == "Hello world!"


def test_form_updates_provider_button_color(admin_client, provider):
    admin_client.post(
        reverse("misago:admin:settings:socialauth:edit", kwargs={"pk": provider.pk}),
        {"button_color": "#ff00ff"},
    )

    provider.refresh_from_db()
    assert provider.button_color == "#ff00ff"


def test_form_invalidates_providers_cache(admin_client, provider):
    with assert_invalidates_cache(SOCIALAUTH_CACHE):
        admin_client.post(
            reverse(
                "misago:admin:settings:socialauth:edit", kwargs={"pk": provider.pk}
            ),
            {"is_active": "0"},
        )


def test_form_sets_provider_order_on_setup(admin_client, other_provider):
    admin_client.post(
        reverse("misago:admin:settings:socialauth:edit", kwargs={"pk": "facebook"}),
        {"is_active": "1", "key": "test-key", "secret": "test-secret"},
    )

    provider = SocialAuthProvider.objects.get(pk="facebook")
    assert provider.order == other_provider.order + 1
