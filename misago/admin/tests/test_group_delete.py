from unittest.mock import patch

import pytest
from django.urls import reverse

from ...cache.enums import CacheName
from ...cache.test import assert_invalidates_cache
from ...test import assert_has_error_message
from ...users.models import Group


@patch("misago.users.groups.remove_group_from_users_groups_ids")
def test_custom_group_is_deleted(
    mock_remove_group_from_users_groups_ids, admin_client, custom_group
):
    response = admin_client.post(
        reverse("misago:admin:groups:delete", kwargs={"pk": custom_group.id})
    )
    assert response.status_code == 302

    with pytest.raises(Group.DoesNotExist):
        custom_group.refresh_from_db()


@patch("misago.users.groups.remove_group_from_users_groups_ids")
def test_deleting_group_invalidates_groups_cache(
    mock_remove_group_from_users_groups_ids, admin_client, custom_group
):
    with assert_invalidates_cache(CacheName.GROUPS):
        admin_client.post(
            reverse("misago:admin:groups:delete", kwargs={"pk": custom_group.id})
        )


@patch("misago.users.groups.remove_group_from_users_groups_ids")
def test_deleting_group_invalidates_permissions_cache(
    mock_remove_group_from_users_groups_ids, admin_client, custom_group
):
    with assert_invalidates_cache(CacheName.PERMISSIONS):
        admin_client.post(
            reverse("misago:admin:groups:delete", kwargs={"pk": custom_group.id})
        )


@patch("misago.users.groups.remove_group_from_users_groups_ids")
def test_deleting_group_calls_users_groups_ids_update_task(
    mock_remove_group_from_users_groups_ids, admin_client, custom_group
):
    admin_client.post(
        reverse("misago:admin:groups:delete", kwargs={"pk": custom_group.id})
    )

    mock_remove_group_from_users_groups_ids.delay.assert_called_once_with(
        custom_group.id
    )


def test_protected_group_cant_be_deleted(admin_client, members_group, user):
    response = admin_client.post(
        reverse("misago:admin:groups:delete", kwargs={"pk": members_group.id})
    )
    assert_has_error_message(response, 'Can\'t delete a protected group "Members".')


def test_default_group_cant_be_deleted(admin_client, custom_group):
    custom_group.is_default = True
    custom_group.save()

    response = admin_client.post(
        reverse("misago:admin:groups:delete", kwargs={"pk": custom_group.id})
    )
    assert_has_error_message(
        response, 'Can\'t delete the default group "Custom Group".'
    )


def test_main_group_cant_be_deleted(admin_client, custom_group, user):
    user.set_groups(custom_group)
    user.save()

    response = admin_client.post(
        reverse("misago:admin:groups:delete", kwargs={"pk": custom_group.id})
    )
    assert_has_error_message(
        response,
        "Can't delete \"Custom Group\" group because it's a main group for some users.",
    )


def test_non_existing_group_cant_be_deleted(admin_client):
    response = admin_client.post(
        reverse("misago:admin:groups:delete", kwargs={"pk": 404})
    )
    assert_has_error_message(response, "Requested group does not exist.")
