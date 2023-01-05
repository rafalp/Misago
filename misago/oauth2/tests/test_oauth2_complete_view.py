from django.urls import reverse


def test_oauth2_complete_view_returns_404_if_oauth_is_disabled(client, dynamic_settings):
    assert dynamic_settings.enable_oauth2_client is False

    response = client.get(reverse("misago:oauth2-complete"))
    assert response.status_code == 404
