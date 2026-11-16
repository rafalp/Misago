from unittest.mock import call

import pytest
from django.contrib.auth import get_user_model
from django.core import mail

from ....cache.test import assert_invalidates_cache
from ....test import assert_contains, assert_has_error_message, assert_not_contains
from ... import BANS_CACHE
from ...datadownloads import request_user_data_download
from ...enums import DeleteUserContentAction
from ...models import Ban, DataDownload, DeletedUser
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


def confirm_delete_users(admin_client, users_admin_link, users_ids, **form_data):
    response = admin_client.post(
        users_admin_link,
        data={"action": "delete_users", "selected_items": users_ids},
    )
    assert response.status_code == 200

    data = {
        "action": "delete_users",
        "selected_items": users_ids,
        "finalize": "",
        "content_action": DeleteUserContentAction.LEAVE.value,
        "anonymous_username": "Deleted",
    }
    data.update(form_data)
    return admin_client.post(users_admin_link, data=data)


@pytest.fixture
def users_ids(db):
    return get_multiple_users_ids()


@pytest.fixture
def mock_delete_user(mocker):
    delay = mocker.Mock()
    mocker.patch(
        "misago.users.admin.views.users.delete_user",
        mocker.Mock(delay=delay),
    )
    return delay


def test_multiple_users_can_be_activated_with_mass_action(
    admin_client, users_admin_link
):
    users = create_multiple_users(requires_activation=1)
    admin_client.post(
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
    admin_client.post(
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
    admin_client.post(
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
    admin_client.post(
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

    admin_client.post(
        users_admin_link,
        data={
            "action": "request_data_download",
            "selected_items": [u.id for u in users],
        },
    )

    assert not DataDownload.objects.exclude(id__in=downloads_ids).exists()


def test_multiple_users_can_be_deleted_with_mass_action(
    admin_client, users_admin_link, admin, mock_delete_user
):
    users = create_multiple_users()
    confirm_delete_users(admin_client, users_admin_link, [u.id for u in users])

    calls = [
        call(
            u.id,
            content_action=DeleteUserContentAction.LEAVE,
            anonymous_username="Deleted",
            deleted_by_id=admin.id,
        )
        for u in users
    ]
    mock_delete_user.assert_has_calls(calls, any_order=True)


def test_delete_users_confirmation_page_allows_content_action_and_anonymous_username(
    admin_client, users_admin_link, admin, mock_delete_user
):
    users = create_multiple_users()
    users_ids = [u.id for u in users]

    response = admin_client.post(
        users_admin_link,
        data={"action": "delete_users", "selected_items": users_ids},
    )

    assert response.status_code == 200
    for user in users:
        assert_contains(
            response,
            f'name="selected_items" value="{user.pk}" checked',
        )
    assert_contains(response, 'name="anonymous_username"')
    assert_contains(response, 'value="Deleted"')
    assert response.content.decode("utf-8").count('name="finalize"') == 1
    mock_delete_user.assert_not_called()

    confirm_delete_users(
        admin_client,
        users_admin_link,
        users_ids,
        content_action=DeleteUserContentAction.DELETE.value,
        anonymous_username="Anonymized",
    )

    calls = [
        call(
            user.id,
            content_action=DeleteUserContentAction.DELETE,
            anonymous_username="Anonymized",
            deleted_by_id=admin.id,
        )
        for user in users
    ]
    mock_delete_user.assert_has_calls(calls, any_order=True)


def test_mass_action_records_users_deletion_by_admin(
    admin_client, users_admin_link, mock_delete_user
):
    from ...deletesrecord import record_user_deleted_by_staff

    mock_delete_user.side_effect = lambda x, **y: record_user_deleted_by_staff()
    users = create_multiple_users()
    confirm_delete_users(admin_client, users_admin_link, [u.id for u in users])

    deleted_count = DeletedUser.objects.filter(
        deleted_by=DeletedUser.DELETED_BY_STAFF
    ).count()
    mock_delete_user.count_call(deleted_count)
    assert deleted_count == len(users)


def test_delete_users_mass_action_fails_if_user_tries_to_delete_themselves(
    admin_client, users_admin_link, admin
):
    response = admin_client.post(
        users_admin_link,
        data={"action": "delete_users", "selected_items": [admin.id]},
    )
    assert_has_error_message(response)
    admin.refresh_from_db()


def test_delete_users_mass_action_fails_if_user_tries_to_delete_staff_members(
    admin_client, users_admin_link
):
    users = create_multiple_users(is_staff=True)
    response = admin_client.post(
        users_admin_link,
        data={"action": "delete_users", "selected_items": [u.id for u in users]},
    )
    assert_has_error_message(response)

    for user in users:
        user.refresh_from_db()


def test_delete_users_mass_action_fails_if_user_tries_to_delete_admins(
    admin_client, users_admin_link, admins_group
):
    users = create_multiple_users()
    for user in users:
        user.set_groups(admins_group)
        user.save()

    response = admin_client.post(
        users_admin_link,
        data={"action": "delete_users", "selected_items": [u.id for u in users]},
    )
    assert_has_error_message(response)

    for user in users:
        user.refresh_from_db()


def test_delete_users_mass_action_fails_if_user_tries_to_delete_root_admins(
    admin_client, users_admin_link
):
    users = create_multiple_users(is_misago_root=True)
    response = admin_client.post(
        users_admin_link,
        data={"action": "delete_users", "selected_items": [u.id for u in users]},
    )
    assert_has_error_message(response)

    for user in users:
        user.refresh_from_db()
