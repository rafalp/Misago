from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...test import assert_contains


@override_dynamic_settings(enable_oauth2_client=True)
def test_account_email_returns_error_if_oauth_client_is_enabled(db, client):
    response = client.get(reverse("misago:account-email"))
    assert response.status_code == 404


def test_account_email_displays_login_required_page_to_anonymous_user(db, client):
    response = client.get(reverse("misago:account-email"))
    assert_contains(response, "Sign in to change your settings", status_code=401)


def test_account_email_renders_form(user_client):
    response = user_client.get(reverse("misago:account-email"))
    assert_contains(response, "Change email address")


def test_account_email_form_sends_email_confirmation_link_on_change(
    user_client, user_password, mailoutbox
):
    response = user_client.post(
        reverse("misago:account-email"),
        {
            "current_password": user_password,
            "new_email": "new@example.com",
            "confirm_email": "new@example.com",
        },
    )
    assert response.status_code == 302

    assert len(mailoutbox) == 1


def test_account_email_form_redirects_to_message_page_on_change(
    user_client, user_password
):
    response = user_client.post(
        reverse("misago:account-email"),
        {
            "current_password": user_password,
            "new_email": "new@example.com",
            "confirm_email": "new@example.com",
        },
    )
    assert response.status_code == 302

    response = user_client.get(response.headers["location"])
    assert_contains(response, "Confirm email address change")


def test_account_email_form_validates_current_password(user_client):
    response = user_client.post(
        reverse("misago:account-email"),
        {
            "current_password": "invalid",
            "new_email": "new@example.com",
            "confirm_email": "new@example.com",
        },
    )
    assert response.status_code == 200
    assert_contains(response, "Change email address")
    assert_contains(response, "Password is incorrect.")


def test_account_email_form_validates_new_email(user_client, user_password):
    response = user_client.post(
        reverse("misago:account-email"),
        {
            "current_password": user_password,
            "new_email": "invalid",
            "confirm_email": "invalid",
        },
    )
    assert response.status_code == 200
    assert_contains(response, "Change email address")
    assert_contains(response, "Enter a valid email address.")


def test_account_email_form_validates_email_is_new(user, user_client, user_password):
    response = user_client.post(
        reverse("misago:account-email"),
        {
            "current_password": user_password,
            "new_email": user.email,
            "confirm_email": user.email,
        },
    )
    assert response.status_code == 200
    assert_contains(response, "This email address is the same as the current one.")


def test_account_email_form_validates_new_emails_match(user_client, user_password):
    response = user_client.post(
        reverse("misago:account-email"),
        {
            "current_password": user_password,
            "new_email": "new@example.com",
            "confirm_email": "other@example.com",
        },
    )
    assert response.status_code == 200
    assert_contains(response, "Change email address")
    assert_contains(response, "New email addresses don&#x27;t match.")


def test_account_email_form_displays_message_page_on_change_in_htmx(
    user_client, user_password
):
    response = user_client.post(
        reverse("misago:account-email"),
        {
            "current_password": user_password,
            "new_email": "new@example.com",
            "confirm_email": "new@example.com",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200
    assert_contains(response, "Confirm email address change")
