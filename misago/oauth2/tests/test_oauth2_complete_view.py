from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...test import assert_contains
from ...users.bans import ban_ip


def test_oauth2_complete_view_returns_404_if_oauth_is_disabled(
    client, dynamic_settings
):
    assert dynamic_settings.enable_oauth2_client is False

    response = client.get(reverse("misago:oauth2-complete"))
    assert response.status_code == 404


def test_oauth2_complete_view_returns_error_404_if_user_ip_is_banned_and_oauth_is_disabled(
    client, dynamic_settings
):
    ban_ip("127.*", "Ya got banned!")

    assert dynamic_settings.enable_oauth2_client is False

    response = client.get(reverse("misago:oauth2-complete"))
    assert response.status_code == 404


@override_dynamic_settings(
    enable_oauth2_client=True,
    oauth2_client_id="clientid123",
    oauth2_scopes="scopes",
    oauth2_login_url="https://example.com/oauth2/login",
)
def test_oauth2_complete_view_returns_error_403_if_user_ip_is_banned(
    client, dynamic_settings
):
    ban_ip("127.*", "Ya got banned!")

    assert dynamic_settings.enable_oauth2_client is True

    response = client.get(reverse("misago:oauth2-complete"))
    assert_contains(response, "Ya got banned", 403)
