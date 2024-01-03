from django.urls import reverse

from ...cache.enums import CacheName
from ...cache.test import assert_invalidates_cache
from ...permissions.models import Moderator
from ...test import assert_has_error_message


def test_make_default_group_changes_default_group(
    admin_client, members_group, custom_group
):
    assert members_group.is_default
    assert not custom_group.is_default

    response = admin_client.post(
        reverse("misago:admin:groups:default", kwargs={"pk": custom_group.pk})
    )
    assert response.status_code == 302

    custom_group.refresh_from_db()
    assert custom_group.is_default

    members_group.refresh_from_db()
    assert not members_group.is_default


def test_make_default_group_invalidates_groups_cache(
    admin_client, members_group, custom_group
):
    with assert_invalidates_cache(CacheName.GROUPS):
        admin_client.post(
            reverse("misago:admin:groups:default", kwargs={"pk": custom_group.pk})
        )


def test_make_default_group_handles_nonexisting_group(admin_client):
    response = admin_client.post(
        reverse("misago:admin:groups:default", kwargs={"pk": 404})
    )
    assert response.status_code == 302
    assert_has_error_message(response, "Requested group does not exist.")


def test_make_default_group_handles_already_default_group(admin_client, members_group):
    response = admin_client.post(
        reverse("misago:admin:groups:default", kwargs={"pk": members_group.id})
    )
    assert response.status_code == 302
    assert_has_error_message(response, '"Members" group is already the default.')


def test_make_default_group_rejects_admins_group(admin_client, admins_group):
    response = admin_client.post(
        reverse("misago:admin:groups:default", kwargs={"pk": admins_group.id})
    )
    assert response.status_code == 302
    assert_has_error_message(
        response, '"Administrators" group can\'t be set as default.'
    )


def test_make_default_group_rejects_moderators_group(admin_client, moderators_group):
    response = admin_client.post(
        reverse("misago:admin:groups:default", kwargs={"pk": moderators_group.id})
    )
    assert response.status_code == 302
    assert_has_error_message(response, '"Moderators" group can\'t be set as default.')


def test_make_default_group_rejects_guests_group(admin_client, guests_group):
    response = admin_client.post(
        reverse("misago:admin:groups:default", kwargs={"pk": guests_group.id})
    )
    assert response.status_code == 302
    assert_has_error_message(response, '"Guests" group can\'t be set as default.')


def test_make_default_group_rejects_custom_moderators_group(admin_client, custom_group):
    Moderator.objects.create(group=custom_group, is_global=True)

    response = admin_client.post(
        reverse("misago:admin:groups:default", kwargs={"pk": custom_group.id})
    )
    assert response.status_code == 302
    assert_has_error_message(
        response,
        'Can\'t set "Custom Group" group as default because it has moderator permissions.',
    )
