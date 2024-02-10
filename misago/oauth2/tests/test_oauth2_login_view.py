from unittest.mock import patch
from urllib.parse import urlparse

from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...test import assert_contains
from ...users.bans import ban_ip


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
    assert "code_challenge" not in redirect_to.query
    assert "code_challenge_method=S256" not in redirect_to.query


@override_dynamic_settings(
    enable_oauth2_client=True,
    oauth2_client_id="clientid123",
    oauth2_scopes="scopes",
    oauth2_login_url="https://example.com/oauth2/login",
)
def test_oauth2_login_view_returns_error_403_if_user_ip_is_banned(
    client, dynamic_settings
):
    ban_ip("127.*", "Ya got banned!")

    assert dynamic_settings.enable_oauth2_client is True

    response = client.get(reverse("misago:oauth2-login"))
    assert_contains(response, "Ya got banned", 403)


def test_oauth2_login_view_returns_error_404_if_user_ip_is_banned_and_oauth_is_disabled(
    client, dynamic_settings
):
    ban_ip("127.*", "Ya got banned!")

    assert dynamic_settings.enable_oauth2_client is False

    response = client.get(reverse("misago:oauth2-login"))
    assert response.status_code == 404


@override_dynamic_settings(
    enable_oauth2_client=True,
    oauth2_client_id="clientid123",
    oauth2_scopes="scopes",
    oauth2_login_url="https://example.com/oauth2/login",
    oauth2_enable_pkce=True,
)
def test_oauth2_login_view_returns_redirect_302_if_oauth_and_pkce_enabled(
    client, dynamic_settings
):
    assert dynamic_settings.enable_oauth2_client is True
    with patch(
        "misago.oauth2.client.get_code_challenge",
        return_value="eemb2YInusdSF01jhCXpzV_juX3_xdAQnVU1oCvFBA",
    ):
        response = client.get(reverse("misago:oauth2-login"))
    assert response.status_code == 302

    redirect_to = urlparse(response["Location"])
    assert redirect_to.netloc == "example.com"
    assert redirect_to.path == "/oauth2/login"
    assert "clientid123" in redirect_to.query
    assert (
        "code_challenge=eemb2YInusdSF01jhCXpzV_juX3_xdAQnVU1oCvFBA" in redirect_to.query
    )
    assert "code_challenge_method=S256" in redirect_to.query
