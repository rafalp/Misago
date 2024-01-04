from django.urls import reverse

from ...cache.enums import CacheName
from ...cache.test import assert_invalidates_cache
from ...test import assert_contains

groups_list = reverse("misago:admin:groups:index")


def test_groups_link_is_registered_in_admin_nav(admin_client):
    response = admin_client.get(reverse("misago:admin:index"))
    assert_contains(response, groups_list)


def test_groups_list_renders(
    admin_client, admins_group, moderators_group, members_group, guests_group
):
    response = admin_client.get(groups_list)
    assert_contains(response, admins_group.name)
    assert_contains(response, moderators_group.name)
    assert_contains(response, members_group.name)
    assert_contains(response, guests_group.name)


def test_groups_can_be_reordered(
    admin_client, admins_group, moderators_group, members_group, guests_group
):
    response = admin_client.post(
        reverse("misago:admin:groups:ordering"),
        {
            "item": [
                str(members_group.id),
                str(guests_group.id),
                str(admins_group.id),
                str(moderators_group.id),
            ],
        },
    )
    assert response.status_code == 204

    admins_group.refresh_from_db()
    assert admins_group.ordering == 2

    moderators_group.refresh_from_db()
    assert moderators_group.ordering == 3

    members_group.refresh_from_db()
    assert members_group.ordering == 0

    guests_group.refresh_from_db()
    assert guests_group.ordering == 1


def test_reordering_groups_invalidates_groups_cache(
    admin_client, admins_group, moderators_group, members_group, guests_group
):
    with assert_invalidates_cache(CacheName.GROUPS):
        admin_client.post(
            reverse("misago:admin:groups:ordering"),
            {
                "item": [
                    str(members_group.id),
                    str(guests_group.id),
                    str(admins_group.id),
                    str(moderators_group.id),
                ],
            },
        )
