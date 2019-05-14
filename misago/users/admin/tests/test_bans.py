from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from ....admin.test import AdminTestCase
from ....cache.test import assert_invalidates_cache
from ....test import assert_contains
from ... import BANS_CACHE
from ...models import Ban


@pytest.fixture
def admin_link(admin_client):
    response = admin_client.get(reverse("misago:admin:users:bans:index"))
    return response["location"]


@pytest.fixture
def ban(db):
    return Ban.objects.create(banned_value="banned_username")


def test_link_is_registered_in_admin_nav(admin_client):
    response = admin_client.get(reverse("misago:admin:users:index"))
    response = admin_client.get(response["location"])
    assert_contains(response, reverse("misago:admin:users:bans:index"))


def test_list_renders_empty(admin_client, admin_link):
    response = admin_client.get(admin_link)
    assert response.status_code == 200


def test_list_renders_with_item(admin_client, admin_link, ban):
    response = admin_client.get(admin_link)
    assert_contains(response, ban.banned_value)


def test_bans_can_be_mass_deleted(admin_client, admin_link):
    bans_ids = [Ban.objects.create(banned_value="ban_%s" % i).id for i in range(10)]

    admin_client.post(admin_link, data={"action": "delete", "selected_items": bans_ids})

    assert Ban.objects.count() == 0


def test_mass_deleting_bans_invalidates_bans_cache(admin_client, admin_link, ban):
    with assert_invalidates_cache(BANS_CACHE):
        admin_client.post(
            admin_link, data={"action": "delete", "selected_items": [ban.id]}
        )


def test_ban_can_be_deleted(admin_client, ban):
    admin_client.post(reverse("misago:admin:users:bans:delete", kwargs={"pk": ban.pk}))

    with pytest.raises(Ban.DoesNotExist):
        ban.refresh_from_db()


def test_deleting_ban_invalidates_bans_cache(admin_client, ban):
    with assert_invalidates_cache(BANS_CACHE):
        admin_client.post(
            reverse("misago:admin:users:bans:delete", kwargs={"pk": ban.pk})
        )


def test_new_ban_form_renders(admin_client):
    response = admin_client.get(reverse("misago:admin:users:bans:new"))
    assert response.status_code == 200


def test_new_ban_can_be_created(admin_client):
    test_date = timezone.now() + timedelta(days=180)

    response = admin_client.post(
        reverse("misago:admin:users:bans:new"),
        data={
            "check_type": Ban.EMAIL,
            "banned_value": "test@test.com",
            "user_message": "Lorem ipsum dolor met",
            "staff_message": "Sit amet elit",
            "expires_on": test_date.isoformat(),
        },
    )

    ban = Ban.objects.get()
    assert ban.check_type == Ban.EMAIL
    assert ban.banned_value == "test@test.com"
    assert ban.user_message == "Lorem ipsum dolor met"
    assert ban.staff_message == "Sit amet elit"
    assert ban.expires_on.isoformat() == test_date.isoformat()


def test_new_ban_creation_invalidates_bans_cache(admin_client):
    with assert_invalidates_cache(BANS_CACHE):
        admin_client.post(
            reverse("misago:admin:users:bans:new"),
            data={"check_type": Ban.EMAIL, "banned_value": "test@test.com"},
        )


def test_edit_ban_form_renders(admin_client, ban):
    response = admin_client.get(
        reverse("misago:admin:users:bans:edit", kwargs={"pk": ban.pk})
    )
    assert response.status_code == 200


def test_ban_can_be_edited(admin_client, ban):
    test_date = timezone.now() + timedelta(days=180)

    response = admin_client.post(
        reverse("misago:admin:users:bans:edit", kwargs={"pk": ban.pk}),
        data={
            "check_type": Ban.EMAIL,
            "banned_value": "test@test.com",
            "user_message": "Lorem ipsum dolor met",
            "staff_message": "Sit amet elit",
            "expires_on": test_date.isoformat(),
        },
    )

    ban.refresh_from_db()
    assert ban.check_type == Ban.EMAIL
    assert ban.banned_value == "test@test.com"
    assert ban.user_message == "Lorem ipsum dolor met"
    assert ban.staff_message == "Sit amet elit"
    assert ban.expires_on.isoformat() == test_date.isoformat()


def test_ban_edition_invalidates_bans_cache(admin_client, ban):
    with assert_invalidates_cache(BANS_CACHE):
        admin_client.post(
            reverse("misago:admin:users:bans:edit", kwargs={"pk": ban.pk}),
            data={"check_type": Ban.EMAIL, "banned_value": "test@test.com"},
        )
