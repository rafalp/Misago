from django.urls import reverse

from ...test import assert_contains, assert_has_success_message


def test_account_preferences_displays_login_required_page_to_anonymous_user(db, client):
    response = client.get(reverse("misago:account-preferences"))
    assert_contains(response, "Sign in to change your settings", status_code=401)


def test_account_preferences_renders_form(user_client):
    response = user_client.get(reverse("misago:account-preferences"))
    assert_contains(response, "Change preferences")


def create_form_data(data: dict | None = None) -> dict:
    default_data = {
        "is_hiding_presence": "0",
        "allow_new_private_threads_by": "0",
        "watch_started_threads": "0",
        "watch_replied_threads": "0",
        "watch_new_private_threads_by_followed": "0",
        "watch_new_private_threads_by_other_users": "0",
        "notify_new_private_threads_by_followed": "0",
        "notify_new_private_threads_by_other_users": "0",
    }

    if data:
        default_data.update(data)

    return default_data


def test_account_preferences_form_updates_user_account(user, user_client):
    response = user_client.post(
        reverse("misago:account-preferences"),
        create_form_data(
            {
                "is_hiding_presence": "1",
                "allow_new_private_threads_by": "1",
                "watch_started_threads": "1",
                "watch_replied_threads": "2",
                "watch_new_private_threads_by_followed": "1",
                "watch_new_private_threads_by_other_users": "2",
                "notify_new_private_threads_by_followed": "1",
                "notify_new_private_threads_by_other_users": "2",
            }
        ),
    )

    assert response.status_code == 302
    assert_has_success_message(response, "Preferences updated")

    user.refresh_from_db()
    assert user.is_hiding_presence
    assert user.allow_new_private_threads_by == 1
    assert user.watch_started_threads == 1
    assert user.watch_replied_threads == 2
    assert user.watch_new_private_threads_by_followed == 1
    assert user.watch_new_private_threads_by_other_users == 2
    assert user.notify_new_private_threads_by_followed == 1
    assert user.notify_new_private_threads_by_other_users == 2


def test_account_preferences_form_updates_user_account_in_htmx(user, user_client):
    response = user_client.post(
        reverse("misago:account-preferences"),
        create_form_data(
            {
                "is_hiding_presence": "1",
                "allow_new_private_threads_by": "1",
                "watch_started_threads": "1",
                "watch_replied_threads": "2",
                "watch_new_private_threads_by_followed": "1",
                "watch_new_private_threads_by_other_users": "2",
                "notify_new_private_threads_by_followed": "1",
                "notify_new_private_threads_by_other_users": "2",
            }
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(response, "Preferences updated")

    user.refresh_from_db()
    assert user.is_hiding_presence
    assert user.allow_new_private_threads_by == 1
    assert user.watch_started_threads == 1
    assert user.watch_replied_threads == 2
    assert user.watch_new_private_threads_by_followed == 1
    assert user.watch_new_private_threads_by_other_users == 2
    assert user.notify_new_private_threads_by_followed == 1
    assert user.notify_new_private_threads_by_other_users == 2
