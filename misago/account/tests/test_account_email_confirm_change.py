from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...test import assert_contains
from ..emailchange import create_email_change_token


@override_dynamic_settings(enable_oauth2_client=True)
def test_account_email_confirm_change_returns_error_if_oauth_client_is_enabled(
    user, user_client
):
    response = user_client.get(
        reverse(
            "misago:account-email-confirm-change",
            kwargs={"user_id": user.id, "token": "any"},
        )
    )
    assert response.status_code == 404


def test_account_email_confirm_change_changes_email_if_user_is_guest(user, client):
    new_email = "new@example.com"
    token = create_email_change_token(user, new_email)
    response = client.get(
        reverse(
            "misago:account-email-confirm-change",
            kwargs={"user_id": user.id, "token": token},
        )
    )
    assert_contains(response, "your email has been changed")

    user.refresh_from_db()
    assert user.email == new_email


def test_account_email_confirm_change_changes_email_if_user_is_authenticated(
    user, user_client
):
    new_email = "new@example.com"
    token = create_email_change_token(user, new_email)
    response = user_client.get(
        reverse(
            "misago:account-email-confirm-change",
            kwargs={"user_id": user.id, "token": token},
        )
    )
    assert_contains(response, "your email has been changed")

    user.refresh_from_db()
    assert user.email == new_email


def test_account_email_confirm_change_returns_error_if_user_id_is_invalid(user, client):
    response = client.get(
        reverse(
            "misago:account-email-confirm-change",
            kwargs={"user_id": user.id + 1, "token": "invalid"},
        )
    )
    assert response.status_code == 404


def test_account_email_confirm_change_returns_error_if_token_is_invalid(user, client):
    response = client.get(
        reverse(
            "misago:account-email-confirm-change",
            kwargs={"user_id": user.id, "token": "invalid"},
        )
    )
    assert_contains(response, "Mail change confirmation link is invalid.")


def test_account_email_confirm_change_returns_error_if_token_email_is_invalid(
    admin, user, client
):
    token = create_email_change_token(user, admin.email)
    response = client.get(
        reverse(
            "misago:account-email-confirm-change",
            kwargs={"user_id": user.id, "token": token},
        )
    )
    assert_contains(response, "This e-mail address is not available.")
