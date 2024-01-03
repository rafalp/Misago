import pytest
from django.urls import reverse

from ...cache.enums import CacheName
from ...cache.test import assert_invalidates_cache
from ...permissions.models import CategoryGroupPermission
from ...users.models import Group


def test_new_group_form_is_rendered(admin_client):
    response = admin_client.get(reverse("misago:admin:groups:new"))
    assert response.status_code == 200


def test_new_group_form_creates_new_group(admin_client):
    response = admin_client.post(
        reverse("misago:admin:groups:new"),
        {"name": "New Group"},
    )
    assert response.status_code == 302

    Group.objects.get(slug="new-group")


def test_new_group_form_copies_group_permissions(
    admin_client, members_group, other_category
):
    CategoryGroupPermission.objects.create(
        group=members_group,
        category=other_category,
        permission="copied",
    )

    response = admin_client.post(
        reverse("misago:admin:groups:new"),
        {"name": "New Group", "copy_permissions": str(members_group.id)},
    )
    assert response.status_code == 302

    new_group = Group.objects.get(slug="new-group")
    CategoryGroupPermission.objects.get(
        group=new_group,
        category=other_category,
        permission="copied",
    )


def test_new_group_form_invalidates_groups_cache(admin_client):
    with assert_invalidates_cache(CacheName.GROUPS):
        admin_client.post(
            reverse("misago:admin:groups:new"),
            {"name": "New Group"},
        )


def test_new_group_form_invalidates_permissions_cache(admin_client):
    with assert_invalidates_cache(CacheName.PERMISSIONS):
        admin_client.post(
            reverse("misago:admin:groups:new"),
            {"name": "New Group"},
        )
