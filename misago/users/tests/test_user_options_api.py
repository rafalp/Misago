import pytest

from ...notifications.threads import ThreadNotifications


@pytest.fixture
def api_link(user):
    return f"/api/users/{user.id}/forum-options/"


def test_change_user_options_api_returns_error_for_guests(db, client, api_link):
    response = client.post(api_link)
    assert response.status_code == 403


def test_change_user_options_api_returns_error_for_empty_post(user_client, api_link):
    response = user_client.post(api_link)

    assert response.status_code == 400
    assert response.json() == {
        "limits_private_thread_invites_to": ["This field is required."],
        "watch_started_threads": ["This field is required."],
        "watch_replied_threads": ["This field is required."],
        "watch_new_private_threads_by_followed": ["This field is required."],
        "watch_new_private_threads_by_other_users": ["This field is required."],
        "notify_new_private_threads_by_followed": ["This field is required."],
        "notify_new_private_threads_by_other_users": ["This field is required."],
    }


def test_change_user_options_api_returns_error_for_invalid_data(user_client, api_link):
    response = user_client.post(
        api_link,
        data={
            "limits_private_thread_invites_to": 100,
            "watch_started_threads": 200,
            "watch_replied_threads": 300,
            "watch_new_private_threads_by_followed": 400,
            "watch_new_private_threads_by_other_users": 500,
            "notify_new_private_threads_by_followed": 600,
            "notify_new_private_threads_by_other_users": 700,
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "limits_private_thread_invites_to": ['"100" is not a valid choice.'],
        "watch_started_threads": ['"200" is not a valid choice.'],
        "watch_replied_threads": ['"300" is not a valid choice.'],
        "watch_new_private_threads_by_followed": ['"400" is not a valid choice.'],
        "watch_new_private_threads_by_other_users": ['"500" is not a valid choice.'],
        "notify_new_private_threads_by_followed": ['"600" is not a valid choice.'],
        "notify_new_private_threads_by_other_users": ['"700" is not a valid choice.'],
    }


def test_change_user_options_api_changes_user_options(user_client, api_link, user):
    NOTIFY_NONE = ThreadNotifications.NONE
    NOTIFY_SITE_ONLY = ThreadNotifications.SITE_ONLY
    NOTIFY_SITE_AND_EMAIL = ThreadNotifications.SITE_AND_EMAIL

    response = user_client.post(
        api_link,
        data={
            "limits_private_thread_invites_to": 0,
            "watch_started_threads": NOTIFY_NONE,
            "watch_replied_threads": NOTIFY_NONE,
            "watch_new_private_threads_by_followed": NOTIFY_NONE,
            "watch_new_private_threads_by_other_users": NOTIFY_NONE,
            "notify_new_private_threads_by_followed": NOTIFY_NONE,
            "notify_new_private_threads_by_other_users": NOTIFY_NONE,
        },
    )
    assert response.status_code == 200

    user.refresh_from_db()

    assert not user.is_hiding_presence
    assert user.limits_private_thread_invites_to == 0
    assert user.watch_started_threads == NOTIFY_NONE
    assert user.watch_replied_threads == NOTIFY_NONE
    assert user.watch_new_private_threads_by_followed == NOTIFY_NONE
    assert user.watch_new_private_threads_by_other_users == NOTIFY_NONE
    assert user.notify_new_private_threads_by_followed == NOTIFY_NONE
    assert user.notify_new_private_threads_by_other_users == NOTIFY_NONE

    response = user_client.post(
        api_link,
        data={
            "is_hiding_presence": False,
            "limits_private_thread_invites_to": 1,
            "watch_started_threads": NOTIFY_SITE_ONLY,
            "watch_replied_threads": NOTIFY_SITE_ONLY,
            "watch_new_private_threads_by_followed": NOTIFY_SITE_ONLY,
            "watch_new_private_threads_by_other_users": NOTIFY_SITE_ONLY,
            "notify_new_private_threads_by_followed": NOTIFY_SITE_ONLY,
            "notify_new_private_threads_by_other_users": NOTIFY_SITE_ONLY,
        },
    )
    assert response.status_code == 200

    user.refresh_from_db()

    assert not user.is_hiding_presence
    assert user.limits_private_thread_invites_to == 1
    assert user.watch_started_threads == NOTIFY_SITE_ONLY
    assert user.watch_replied_threads == NOTIFY_SITE_ONLY
    assert user.watch_new_private_threads_by_followed == NOTIFY_SITE_ONLY
    assert user.watch_new_private_threads_by_other_users == NOTIFY_SITE_ONLY
    assert user.notify_new_private_threads_by_followed == NOTIFY_SITE_ONLY
    assert user.notify_new_private_threads_by_other_users == NOTIFY_SITE_ONLY

    response = user_client.post(
        api_link,
        data={
            "is_hiding_presence": True,
            "limits_private_thread_invites_to": 2,
            "watch_started_threads": NOTIFY_SITE_AND_EMAIL,
            "watch_replied_threads": NOTIFY_SITE_AND_EMAIL,
            "watch_new_private_threads_by_followed": NOTIFY_SITE_AND_EMAIL,
            "watch_new_private_threads_by_other_users": NOTIFY_SITE_AND_EMAIL,
            "notify_new_private_threads_by_followed": NOTIFY_SITE_AND_EMAIL,
            "notify_new_private_threads_by_other_users": NOTIFY_SITE_AND_EMAIL,
        },
    )
    assert response.status_code == 200

    user.refresh_from_db()

    assert user.is_hiding_presence
    assert user.limits_private_thread_invites_to == 2
    assert user.watch_started_threads == NOTIFY_SITE_AND_EMAIL
    assert user.watch_replied_threads == NOTIFY_SITE_AND_EMAIL
    assert user.watch_new_private_threads_by_followed == NOTIFY_SITE_AND_EMAIL
    assert user.watch_new_private_threads_by_other_users == NOTIFY_SITE_AND_EMAIL
    assert user.notify_new_private_threads_by_followed == NOTIFY_SITE_AND_EMAIL
    assert user.notify_new_private_threads_by_other_users == NOTIFY_SITE_AND_EMAIL
