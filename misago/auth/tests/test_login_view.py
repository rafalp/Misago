from urllib.parse import quote_plus

from django.test import override_settings
from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...test import assert_contains, assert_not_contains
from ...users.models import Ban


def test_login_view_displays_login_form_to_anonymous_users(db, client):
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


@override_dynamic_settings(
    enable_oauth2_client=True,
    oauth2_provider="OAuth2",
)
def test_login_view_displays_delegated_page_if_auth_is_delegated(db, client):
    response = client.get(reverse("misago:login"))
    assert_contains(response, "page-login")
    assert_contains(response, "Sign in")
    assert_contains(response, "Sign in with OAuth2")


def test_login_view_shows_error_if_username_is_missing(db, client):
    response = client.post(reverse("misago:login"), {"password": "password"})
    assert_contains(response, "Fill out all fields.")


def test_login_view_shows_error_if_password_is_missing(db, client):
    response = client.post(reverse("misago:login"), {"username": "username"})
    assert_contains(response, "Fill out all fields.")


def test_login_view_shows_error_if_username_and_password_is_missing(db, client):
    response = client.post(reverse("misago:login"))
    assert_contains(response, "Fill out all fields.")


def test_login_view_shows_error_if_username_is_invalid(db, client):
    response = client.post(
        reverse("misago:login"),
        {"username": "invalid", "password": "invalid"},
    )
    assert_contains(response, "Login or password is incorrect.")


def test_login_view_shows_error_if_password_is_invalid(client, user):
    response = client.post(
        reverse("misago:login"),
        {"username": user.username, "password": "invalid"},
    )
    assert_contains(response, "Login or password is incorrect.")


def test_login_view_shows_error_if_user_account_is_deactivated(
    client, user, user_password
):
    user.is_active = False
    user.save()

    response = client.post(
        reverse("misago:login"),
        {"username": user.username, "password": user_password},
    )
    assert_contains(response, "Login or password is incorrect.")


def test_login_view_displays_banned_page_to_banned_users(client, user, user_password):
    ban = Ban.objects.create(
        banned_value=user.username,
        check_type=Ban.USERNAME,
        user_message="This is a test ban.",
    )

    response = client.post(
        reverse("misago:login"),
        {
            "username": user.email,
            "password": user_password,
        },
    )
    assert_contains(response, ban.user_message, status_code=403)


def test_login_view_excludes_root_misago_admins_from_ban_check(
    client, root_admin, user_password
):
    Ban.objects.create(
        banned_value=root_admin.username,
        check_type=Ban.USERNAME,
        user_message="This is a test ban.",
    )

    response = client.post(
        reverse("misago:login"),
        {
            "username": root_admin.email,
            "password": user_password,
        },
    )

    response = client.get(reverse("misago:index"))
    assert_contains(response, root_admin.username)


def test_login_view_excludes_misago_admins_from_ban_check(
    client, secondary_admin, user_password
):
    Ban.objects.create(
        banned_value=secondary_admin.username,
        check_type=Ban.USERNAME,
        user_message="This is a test ban.",
    )

    response = client.post(
        reverse("misago:login"),
        {
            "username": secondary_admin.email,
            "password": user_password,
        },
    )

    response = client.get(reverse("misago:index"))
    assert_contains(response, secondary_admin.username)


def test_login_view_shows_error_if_user_needs_admin_activation(
    client, user, user_password
):
    user.requires_activation = user.ACTIVATION_ADMIN
    user.save()

    response = client.post(
        reverse("misago:login"),
        {"username": user.username, "password": user_password},
    )
    assert_contains(response, "A site administrator has to activate your account")


def test_login_view_shows_error_if_user_needs_user_activation(
    client, user, user_password
):
    user.requires_activation = user.ACTIVATION_USER
    user.save()

    response = client.post(
        reverse("misago:login"),
        {"username": user.username, "password": user_password},
    )
    assert_contains(response, "You have to activate your account")
