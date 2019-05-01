from django.contrib.auth import get_user_model
from django.core import mail

from ....cache.test import assert_invalidates_cache
from ....test import assert_contains, assert_not_contains
from ... import BANS_CACHE
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


def test_multiple_users_can_be_activated_with_mass_action(
    admin_client, users_admin_link
):
    users_ids = get_multiple_users_ids(requires_activation=1)
    response = admin_client.post(
        users_admin_link, data={"action": "activate", "selected_items": users_ids}
    )

    assert not User.objects.filter(id__in=users_ids, requires_activation=1).exists()


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
    admin_client, users_admin_link
):
    users_ids = get_multiple_users_ids()
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
    admin_client, users_admin_link
):
    users_ids = get_multiple_users_ids()
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
