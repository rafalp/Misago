from django.urls import reverse


def test_view_begins_social_auth_for_provider(client, provider):
    response = client.get(
        reverse("misago:social-begin", kwargs={"backend": provider.pk})
    )
    assert response.status_code == 302


def test_view_returns_404_for_disabled_provider(client, disabled_provider):
    response = client.get(
        reverse("misago:social-begin", kwargs={"backend": disabled_provider.pk})
    )
    assert response.status_code == 404


def test_view_returns_404_for_undefined_provider(db, client):
    response = client.get(
        reverse("misago:social-begin", kwargs={"backend": "undefined"})
    )
    assert response.status_code == 404
