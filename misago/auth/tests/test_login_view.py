from urllib.parse import quote_plus

from django.test import override_settings
from django.urls import reverse

from ...test import assert_contains, assert_not_contains


def test_login_view_displays_login_form_to_guests(db, client):
    response = client.get(reverse("misago:login"))
    assert_contains(response, "page-login")
    assert_contains(response, "Sign in")


def test_login_view_authenticates_user_by_username(client, user, user_password):
    response = client.post(
        reverse("misago:login"),
        {"username": user.username, "password": user_password},
    )
    assert response.status_code == 302

    response = client.get(reverse("misago:index"))
    assert_contains(response, user.username)


def test_login_view_authenticates_user_by_email(client, user, user_password):
    response = client.post(
        reverse("misago:login"),
        {"username": user.email, "password": user_password},
    )
    assert response.status_code == 302

    response = client.get(reverse("misago:index"))
    assert_contains(response, user.username)


def test_login_view_redirects_authenticated_user_by_post_value(
    client, user, user_password
):
    response = client.post(
        reverse("misago:login"),
        {
            "username": user.email,
            "password": user_password,
            "next": reverse("misago:account-preferences"),
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:account-preferences")

    response = client.get(reverse("misago:index"))
    assert_contains(response, user.username)


def test_login_view_redirects_authenticated_user_by_query_parameter(
    client, user, user_password
):
    response = client.post(
        reverse("misago:login")
        + "?next="
        + quote_plus(reverse("misago:account-preferences")),
        {
            "username": user.email,
            "password": user_password,
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:account-preferences")

    response = client.get(reverse("misago:index"))
    assert_contains(response, user.username)


def test_login_view_redirects_already_authenticated_user(user_client):
    response = user_client.post(reverse("misago:login"))
    assert response.status_code == 302
    assert response["location"] == reverse("misago:index")


def test_login_view_redirects_already_authenticated_user_by_post_value(user_client):
    response = user_client.post(
        reverse("misago:login"),
        {
            "next": reverse("misago:account-preferences"),
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:account-preferences")


def test_login_view_redirects_already_authenticated_user_by_query_parameter(
    user_client,
):
    response = user_client.get(
        reverse("misago:login")
        + "?next="
        + quote_plus(reverse("misago:account-preferences"))
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:account-preferences")


def test_login_view_displays_social_auth_buttons(
    social_auth_github, social_auth_facebook, client
):
    response = client.get(reverse("misago:login"))
    assert_contains(response, "page-login")
    assert_contains(response, "Sign in")
    assert_contains(response, "Sign in with GitHub")
    assert_contains(response, "Sign in with Facebook")
    assert_not_contains(response, "Sign in with X")


@override_settings(LOGIN_URL="/other/login/")
def test_login_view_is_not_available_if_custom_login_url_is_set(db, client):
    response = client.get(reverse("misago:login"))
    assert response.status_code == 404
