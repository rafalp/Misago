from django.test import override_settings
from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...test import assert_contains, assert_not_contains


def test_require_login_decorator_displays_login_required_page_to_anonymous_user(
    db, client
):
    response = client.get(reverse("misago:account-preferences"))
    assert_contains(response, "page-login", status_code=401)
    assert_contains(response, "Sign in", status_code=401)


def test_require_login_decorator_displays_view_to_authenticated(user_client):
    response = user_client.get(reverse("misago:account-preferences"))
    assert_not_contains(response, "page-login")


def test_require_login_decorator_authenticates_user_by_username(
    client, user, user_password
):
    response = client.post(
        reverse("misago:account-preferences"),
        {"username": user.username, "password": user_password},
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:account-preferences")


@override_settings(LOGIN_URL="/other/login/")
def test_require_login_decorator_displays_permisison_denied_if_custom_login_page_is_enabled(
    db, client
):
    response = client.get(reverse("misago:account-preferences"))
    assert response.status_code == 403


@override_dynamic_settings(
    enable_oauth2_client=True,
    oauth2_provider="OAuth2",
)
def test_require_login_decorator_displays_delegated_login_form_if_auth_is_delegated(
    db, client
):
    response = client.get(reverse("misago:account-preferences"))
    assert_contains(response, "page-login", status_code=401)
    assert_contains(response, "Sign in", status_code=401)
    assert_contains(response, "Sign in with OAuth2", status_code=401)
