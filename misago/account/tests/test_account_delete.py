from unittest.mock import patch

from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...test import assert_contains


@override_dynamic_settings(enable_oauth2_client=True, allow_delete_own_account=True)
def test_account_delete_returns_error_if_oauth_client_is_enabled(db, client):
    response = client.get(reverse("misago:account-delete"))
    assert response.status_code == 404


@override_dynamic_settings(enable_oauth2_client=False, allow_delete_own_account=False)
def test_account_delete_returns_error_if_own_account_deletion_is_disabled(db, client):
    response = client.get(reverse("misago:account-delete"))
    assert response.status_code == 404


@override_dynamic_settings(enable_oauth2_client=False, allow_delete_own_account=True)
def test_account_delete_displays_login_required_page_to_anonymous_user(db, client):
    response = client.get(reverse("misago:account-delete"))
    assert_contains(response, "Sign in to change your settings", status_code=401)


@override_dynamic_settings(enable_oauth2_client=False, allow_delete_own_account=True)
def test_account_delete_renders_form(user, user_client):
    response = user_client.get(reverse("misago:account-delete"))
    assert_contains(response, "This form allows you to delete your account.")

    user.refresh_from_db()


@override_dynamic_settings(enable_oauth2_client=False, allow_delete_own_account=True)
def test_account_delete_shows_error_if_password_is_incorrect(user, user_client):
    response = user_client.post(
        reverse("misago:account-delete"), {"password": "incorrect"}
    )
    assert_contains(response, "This form allows you to delete your account.")
    assert_contains(response, "Entered password is incorrect.")

    user.refresh_from_db()


@override_dynamic_settings(enable_oauth2_client=False, allow_delete_own_account=True)
def test_account_delete_shows_error_if_user_account_is_protected(
    admin, admin_client, user_password
):
    response = admin_client.post(
        reverse("misago:account-delete"), {"password": user_password}
    )
    assert_contains(response, "This form allows you to delete your account.")
    assert_contains(response, "You can&#x27;t delete your account")

    admin.refresh_from_db()


@override_dynamic_settings(enable_oauth2_client=False, allow_delete_own_account=True)
@patch("misago.account.views.settings.delete_user")
def test_account_delete_calls_delete_user_task(
    delete_user, user, user_client, user_password
):
    response = user_client.post(
        reverse("misago:account-delete"), {"password": user_password}
    )
    response.status_code == 302

    delete_user.delay.assert_called_once_with(user.id)


@override_dynamic_settings(enable_oauth2_client=False, allow_delete_own_account=True)
@patch("misago.account.views.settings.delete_user")
def test_account_delete_redirects_to_delete_complete_page(
    delete_user, user, user_client, user_password
):
    response = user_client.post(
        reverse("misago:account-delete"), {"password": user_password}
    )
    response.status_code == 302

    response = user_client.get(response.headers["location"])
    assert_contains(response, "User, your account is now being deleted.")


@patch("misago.account.views.settings.delete_user")
def test_account_delete_completed_view_returns_404_if_navigated_directly(user_client):
    response = user_client.get(reverse("misago:account-delete-completed"))
    response.status_code == 404
