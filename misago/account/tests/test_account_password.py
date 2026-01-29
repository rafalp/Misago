from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...test import assert_contains, assert_has_success_message


@override_dynamic_settings(enable_oauth2_client=True)
def test_account_password_returns_error_if_oauth_client_is_enabled(db, client):
    response = client.get(reverse("misago:account-password"))
    assert response.status_code == 404


def test_account_password_displays_login_required_page_to_anonymous_user(db, client):
    response = client.get(reverse("misago:account-password"))
    assert_contains(response, "Sign in to change your settings", status_code=401)


def test_account_password_renders_form(user_client):
    response = user_client.get(reverse("misago:account-password"))
    assert_contains(response, "Change password")


def test_account_password_form_changes_password(user, user_client, user_password):
    response = user_client.post(
        reverse("misago:account-password"),
        {
            "current_password": user_password,
            "new_password": "l0r3m1psum",
            "confirm_password": "l0r3m1psum",
        },
    )
    assert response.status_code == 302
    assert_has_success_message(response, "Password changed")

    user.refresh_from_db()
    assert user.check_password("l0r3m1psum")


def test_account_password_form_keeps_user_authenticated_on_change(
    user_client, user_password
):
    response = user_client.post(
        reverse("misago:account-password"),
        {
            "current_password": user_password,
            "new_password": "l0r3m1psum",
            "confirm_password": "l0r3m1psum",
        },
    )
    assert response.status_code == 302
    assert_has_success_message(response, "Password changed")

    response = user_client.get(reverse("misago:account-password"))
    assert_contains(response, "Change password")


def test_account_password_form_sends_email_notification_on_change(
    user_client, user_password, mailoutbox
):
    response = user_client.post(
        reverse("misago:account-password"),
        {
            "current_password": user_password,
            "new_password": "l0r3m1psum",
            "confirm_password": "l0r3m1psum",
        },
    )
    assert response.status_code == 302
    assert_has_success_message(response, "Password changed")

    assert len(mailoutbox) == 1


def test_account_password_form_validates_current_password(
    user, user_client, user_password
):
    response = user_client.post(
        reverse("misago:account-password"),
        {
            "current_password": "invalid",
            "new_password": "l0r3m1psum",
            "confirm_password": "l0r3m1psum",
        },
    )
    assert response.status_code == 200
    assert_contains(response, "Change password")
    assert_contains(response, "Password is incorrect.")

    user.refresh_from_db()
    assert user.check_password(user_password)


def test_account_password_form_validates_new_password(user, user_client, user_password):
    response = user_client.post(
        reverse("misago:account-password"),
        {
            "current_password": user_password,
            "new_password": "p",
            "confirm_password": "p",
        },
    )
    assert response.status_code == 200
    assert_contains(response, "Change password")
    assert_contains(response, "This password is too short.")

    user.refresh_from_db()
    assert user.check_password(user_password)


def test_account_password_form_validates_new_passwords_match(
    user, user_client, user_password
):
    response = user_client.post(
        reverse("misago:account-password"),
        {
            "current_password": user_password,
            "new_password": "l0r3m1psum",
            "confirm_password": "l0r3m1psumdolor",
        },
    )
    assert response.status_code == 200
    assert_contains(response, "Change password")
    assert_contains(response, "New passwords don&#x27;t match.")

    user.refresh_from_db()
    assert user.check_password(user_password)


def test_account_password_form_changes_password_in_htmx(
    user, user_client, user_password
):
    response = user_client.post(
        reverse("misago:account-password"),
        {
            "current_password": user_password,
            "new_password": "l0r3m1psum",
            "confirm_password": "l0r3m1psum",
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Password changed")

    user.refresh_from_db()
    assert user.check_password("l0r3m1psum")
