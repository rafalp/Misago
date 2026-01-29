from unittest.mock import patch

from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...pagination.cursor import EmptyPageError
from ...test import assert_contains, assert_has_success_message, assert_not_contains


@override_dynamic_settings(enable_oauth2_client=True)
def test_account_username_returns_error_if_oauth_client_is_enabled(db, client):
    response = client.get(reverse("misago:account-username"))
    assert response.status_code == 404


def test_account_username_displays_login_required_page_to_anonymous_user(db, client):
    response = client.get(reverse("misago:account-username"))
    assert_contains(response, "Sign in to change your settings", status_code=401)


def test_account_username_renders_form(user_client):
    response = user_client.get(reverse("misago:account-username"))
    assert_contains(response, "Change username")


def test_account_username_form_changes_username(user_client, user):
    response = user_client.post(
        reverse("misago:account-username"), {"username": "JohnDoe"}
    )

    assert response.status_code == 302
    assert_has_success_message(response, "Username changed")

    user.refresh_from_db()
    assert user.username == "JohnDoe"

    change = user.namechanges.first()
    assert change.new_username == "JohnDoe"
    assert change.old_username == "User"


def test_account_username_form_validates_username_is_new(user_client, user):
    response = user_client.post(
        reverse("misago:account-username"), {"username": user.username}
    )

    assert response.status_code == 200
    assert_contains(response, "This username is the same as the current one.")

    user.refresh_from_db()
    assert user.username == "User"


def test_account_username_form_validates_username(user_client, admin, user):
    response = user_client.post(
        reverse("misago:account-username"), {"username": admin.username}
    )

    assert response.status_code == 200
    assert_contains(response, "This username is not available.")

    user.refresh_from_db()
    assert user.username == "User"


def test_account_username_form_validates_username_change_permission(user_client, user):
    user.group.can_change_username = False
    user.group.save()

    response = user_client.post(
        reverse("misago:account-username"), {"username": "JohnDoe"}
    )

    assert response.status_code == 200
    assert_contains(response, "You can't change your username.")

    user.refresh_from_db()
    assert user.username == "User"


def test_account_username_form_validates_username_change_cooldown(user_client, user):
    user.group.username_changes_span = 1
    user.group.save()

    user.set_username("John", user)

    response = user_client.post(
        reverse("misago:account-username"), {"username": "JohnDoe"}
    )

    assert response.status_code == 200
    assert_contains(response, "You can't change your username at the moment.")

    user.refresh_from_db()
    assert user.username == "User"


def test_account_username_renders_message_about_unlimited_username_changes(
    user_client, user
):
    user.group.username_changes_limit = 0
    user.group.save()

    response = user_client.get(reverse("misago:account-username"))
    assert_contains(response, "Change username")
    assert_contains(response, "You can change your username unlimited number of times.")


def test_account_username_renders_message_about_username_changes_disabled(
    user_client, user
):
    user.group.can_change_username = False
    user.group.save()

    response = user_client.get(reverse("misago:account-username"))
    assert_contains(response, "Change username")
    assert_contains(response, "You can't change your username.")


def test_account_username_renders_message_about_username_changes_left(
    user_client, user
):
    user.group.username_changes_limit = 2
    user.group.username_changes_span = 0
    user.group.save()

    user.set_username("John", user)

    response = user_client.get(reverse("misago:account-username"))
    assert_contains(response, "Change username")
    assert_contains(response, "You can change your username 1 more time.")


def test_account_username_renders_message_about_username_change_cooldown(
    user_client, user
):
    user.group.username_changes_span = 1
    user.group.save()

    user.set_username("John", user)

    response = user_client.get(reverse("misago:account-username"))
    assert_contains(response, "Change username")
    assert_contains(response, "You will be able to change your username again")


def test_account_username_renders_empty_history(user_client):
    response = user_client.get(reverse("misago:account-username"))
    assert_contains(response, "Changes history")
    assert_contains(response, "Your account has no history of name changes.")


def test_account_username_renders_history_item(user_client, user):
    orginal_username = user.username
    user.set_username("John", user)

    response = user_client.get(reverse("misago:account-username"))
    assert_contains(response, "Changes history")
    assert_contains(response, orginal_username)
    assert_contains(response, "John")
    assert_not_contains(response, "Your account has no history of name changes.")


@patch(
    "misago.account.views.settings.paginate_queryset", side_effect=EmptyPageError(10)
)
def test_account_username_redirects_to_last_page_for_invalid_cursor(
    mock_pagination, user_client
):
    response = user_client.get(reverse("misago:account-username"))

    assert response.status_code == 302
    assert response["location"] == reverse("misago:account-username") + "?cursor=10"

    mock_pagination.assert_called_once()
