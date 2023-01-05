from urllib.parse import urlparse

from django.urls import reverse

from ...conf.test import override_dynamic_settings


def test_oauth2_login_view_returns_404_if_oauth_is_disabled(client, dynamic_settings):
    assert dynamic_settings.enable_oauth2_client is False

    response = client.get(reverse("misago:oauth2-login"))
    assert response.status_code == 404


@override_dynamic_settings(
    enable_oauth2_client=True,
    oauth2_client_id="clientid123",
    oauth2_scopes="scopes",
    oauth2_login_url="https://example.com/oauth2/login",
)
def test_oauth2_login_view_returns_redirect_302_if_oauth_is_enabled(
    client, dynamic_settings
):
    assert dynamic_settings.enable_oauth2_client is True

    response = client.get(reverse("misago:oauth2-login"))
    assert response.status_code == 302

    redirect_to = urlparse(response["Location"])
    assert redirect_to.netloc == "example.com"
    assert redirect_to.path == "/oauth2/login"
    assert "clientid123" in redirect_to.query
