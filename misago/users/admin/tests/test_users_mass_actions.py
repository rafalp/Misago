from unittest.mock import call

import pytest
from django.contrib.auth import get_user_model
from django.core import mail

from ....cache.test import assert_invalidates_cache
from ....test import assert_contains, assert_has_error_message, assert_not_contains
from ... import BANS_CACHE
from ...datadownloads import request_user_data_download
from ...models import Ban, DataDownload
from ...test import create_test_user

User = get_user_model()


def create_multiple_users(**kwargs):
    return [
        create_test_user("User%s" % i, "user%s@gmail.com" % i, **kwargs)
        for i in range(5)
    ]


def get_multiple_users_ids(**kwargs):
    users = create_multiple_users(**kwargs)
    return [u.id for u in users]


@pytest.fixture
def users_ids(db):
    return get_multiple_users_ids()


def test_multiple_users_can_be_activated_with_mass_action(
    admin_client, users_admin_link
):
    users = create_multiple_users(requires_activation=1)
    response = admin_client.post(
        users_admin_link,
        data={"action": "activate", "selected_items": [u.id for u in users]},
    )

    for user in users:
        user.refresh_from_db()
        assert not user.requires_activation


def test_activating_multiple_users_sends_email_notifications_to_them(
    admin_client, users_admin_link
):
    users_ids = get_multiple_users_ids(requires_activation=1)
    response = admin_client.post(
        users_admin_link, data={"action": "activate", "selected_items": users_ids}
    )

    assert len(mail.outbox) == len(users_ids)
    assert "has been activated" in mail.outbox[0].subject


def test_ban_multiple_users_form_is_rendered(admin_client, users_admin_link):
    users_ids = get_multiple_users_ids()
    response = admin_client.post(
        users_admin_link, data={"action": "ban", "selected_items": users_ids}
    )
    assert response.status_code == 200


def test_multiple_users_can_be_banned_with_mass_action(admin_client, users_admin_link):
    users = create_multiple_users()
    admin_client.post(
        users_admin_link,
        data={
            "action": "ban",
            "selected_items": [u.id for u in users],
            "ban_type": ["usernames", "emails", "domains"],
            "finalize": "",
        },
    )

    for user in users:
        Ban.objects.get(banned_value=user.username.lower())
        Ban.objects.get(banned_value=user.email)
        Ban.objects.get(banned_value="*%s" % user.email[-10:])


def test_option_to_ban_multiple_users_ips_is_disabled_if_user_ips_are_not_available(
    admin_client, users_admin_link, users_ids
):
    response = admin_client.post(
        users_admin_link, data={"action": "ban", "selected_items": users_ids}
    )
    assert_not_contains(response, 'value="ip"')
    assert_not_contains(response, 'value="ip_first"')
    assert_not_contains(response, 'value="ip_two"')


def test_option_to_ban_multiple_users_ips_is_enabled_if_user_ips_are_available(
    admin_client, users_admin_link
):
    users_ids = get_multiple_users_ids(joined_from_ip="1.2.3.4")
    response = admin_client.post(
        users_admin_link, data={"action": "ban", "selected_items": users_ids}
    )
    assert_contains(response, 'value="ip"')
    assert_contains(response, 'value="ip_first"')
    assert_contains(response, 'value="ip_two"')


def test_multiple_users_ips_can_be_banned_with_mass_action(
    admin_client, users_admin_link
):
    users_ids = get_multiple_users_ids(joined_from_ip="1.2.3.4")
    response = admin_client.post(
        users_admin_link,
        data={
            "action": "ban",
            "selected_items": users_ids,
            "ban_type": ["ip", "ip_first", "ip_two"],
            "finalize": "",
        },
    )

    Ban.objects.get(banned_value="1.2.3.4")
    Ban.objects.get(banned_value="1.*")
    Ban.objects.get(banned_value="1.2.*")


def test_banning_multiple_users_with_mass_action_invalidates_bans_cache(
    admin_client, users_admin_link, users_ids
):
    with assert_invalidates_cache(BANS_CACHE):
        admin_client.post(
            users_admin_link,
            data={
                "action": "ban",
                "selected_items": users_ids,
                "ban_type": ["usernames", "emails", "domains"],
                "finalize": "",
            },
        )


def test_data_downloads_can_be_requested_for_multiple_users_with_mass_action(
    admin_client, users_admin_link
):
    users = create_multiple_users()
    response = admin_client.post(
        users_admin_link,
        data={
            "action": "request_data_download",
            "selected_items": [u.id for u in users],
        },
    )

    for user in users:
        DataDownload.objects.get(user=user)


def test_mass_action_is_not_requesting_data_downloads_for_users_with_existing_requests(
    admin_client, users_admin_link
):
    users = create_multiple_users()
    downloads_ids = [request_user_data_download(u).id for u in users]

    response = admin_client.post(
        users_admin_link,
        data={
            "action": "request_data_download",
            "selected_items": [u.id for u in users],
        },
    )

    assert not DataDownload.objects.exclude(id__in=downloads_ids).exists()


def test_multiple_users_can_be_deleted_with_mass_action(admin_client, users_admin_link):
    users = create_multiple_users()
    response = admin_client.post(
        users_admin_link,
        data={"action": "delete_accounts", "selected_items": [u.id for u in users]},
    )

    for user in users:
        with pytest.raises(User.DoesNotExist):
            user.refresh_from_db()


def test_delete_users_mass_action_fails_if_user_tries_to_delete_themselves(
    admin_client, users_admin_link, superuser
):
    response = admin_client.post(
        users_admin_link,
        data={"action": "delete_accounts", "selected_items": [superuser.id]},
    )
    assert_has_error_message(response)
    superuser.refresh_from_db()


def test_delete_users_mass_action_fails_if_user_tries_to_delete_staff_members(
    admin_client, users_admin_link
):
    users = create_multiple_users(is_staff=True)
    response = admin_client.post(
        users_admin_link,
        data={"action": "delete_accounts", "selected_items": [u.id for u in users]},
    )
    assert_has_error_message(response)

    for user in users:
        user.refresh_from_db()


def test_delete_users_mass_action_fails_if_user_tries_to_delete_superusers(
    admin_client, users_admin_link
):
    users = create_multiple_users(is_superuser=True)
    response = admin_client.post(
        users_admin_link,
        data={"action": "delete_accounts", "selected_items": [u.id for u in users]},
    )
    assert_has_error_message(response)

    for user in users:
        user.refresh_from_db()


@pytest.fixture
def mock_delete_user_with_content(mocker):
    delay = mocker.Mock()
    mocker.patch(
        "misago.users.admin.views.users.delete_user_with_content",
        mocker.Mock(delay=delay),
    )
    return delay


def test_multiple_users_can_be_deleted_together_with_content_by_mass_action(
    admin_client, users_admin_link, users_ids, mock_delete_user_with_content
):
    response = admin_client.post(
        users_admin_link, data={"action": "delete_all", "selected_items": users_ids}
    )

    calls = [call(u) for u in users_ids]
    mock_delete_user_with_content.assert_has_calls(calls, any_order=True)


def test_deleting_multiple_users_with_content_disables_their_accounts(
    admin_client, users_admin_link, mock_delete_user_with_content
):
    users = create_multiple_users()
    response = admin_client.post(
        users_admin_link,
        data={"action": "delete_all", "selected_items": [u.id for u in users]},
    )

    for user in users:
        user.refresh_from_db()
        assert not user.is_active


def test_delete_users_with_content_mass_action_fails_if_user_tries_to_delete_themselves(
    admin_client, users_admin_link, superuser, mock_delete_user_with_content
):
    response = admin_client.post(
        users_admin_link,
        data={"action": "delete_all", "selected_items": [superuser.id]},
    )

    assert_has_error_message(response)
    mock_delete_user_with_content.assert_not_called()

    superuser.refresh_from_db()
    assert superuser.is_active


def test_delete_users_with_content_mass_action_fails_if_user_tries_to_delete_staff(
    admin_client, users_admin_link, mock_delete_user_with_content
):
    users = create_multiple_users(is_staff=True)
    response = admin_client.post(
        users_admin_link,
        data={"action": "delete_all", "selected_items": [u.id for u in users]},
    )

    assert_has_error_message(response)
    mock_delete_user_with_content.assert_not_called()

    for user in users:
        user.refresh_from_db()
        assert user.is_active


def test_delete_users_with_content_mass_action_fails_if_user_tries_to_delete_superusers(
    admin_client, users_admin_link, mock_delete_user_with_content
):
    users = create_multiple_users(is_superuser=True)
    response = admin_client.post(
        users_admin_link,
        data={"action": "delete_all", "selected_items": [u.id for u in users]},
    )

    assert_has_error_message(response)
    mock_delete_user_with_content.assert_not_called()

    for user in users:
        user.refresh_from_db()
        assert user.is_active
