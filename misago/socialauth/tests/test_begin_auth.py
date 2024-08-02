from django.urls import reverse

from ...conf.test import override_dynamic_settings


def test_view_begins_social_auth_for_provider(client, provider):
    response = client.get(
        reverse("misago:social-login", kwargs={"backend": provider.pk})
    )
    assert response.status_code == 302


@override_dynamic_settings(
    enable_oauth2_client=True,
    oauth2_provider="Lorem",
)
def test_view_returns_403_when_oauth2_is_enabled(client, provider):
    response = client.get(
        reverse("misago:social-login", kwargs={"backend": provider.pk})
    )
    assert response.status_code == 403


def test_view_returns_404_for_disabled_provider(client, disabled_provider):
    response = client.get(
        reverse("misago:social-login", kwargs={"backend": disabled_provider.pk})
    )
    assert response.status_code == 404


def test_view_returns_404_for_undefined_provider(db, client):
    response = client.get(
        reverse("misago:social-login", kwargs={"backend": "undefined"})
    )
    assert response.status_code == 404
