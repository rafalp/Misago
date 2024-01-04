from django.urls import reverse

from ...permissions.models import Moderator
from ...test import assert_contains

moderators_list = reverse("misago:admin:moderators:index")


def test_moderators_link_is_registered_in_admin_nav(admin_client):
    response = admin_client.get(reverse("misago:admin:index"))
    assert_contains(response, moderators_list)


def test_moderators_list_renders_with_default_groups_moderators(
    admin_client, admins_group, moderators_group
):
    response = admin_client.get(moderators_list)
    assert_contains(response, admins_group.name)
    assert_contains(response, moderators_group.name)


def test_moderators_list_renders_with_custom_group_moderator(
    admin_client, custom_group
):
    Moderator.objects.create(group=custom_group)
    response = admin_client.get(moderators_list)
    assert_contains(response, custom_group.name)


def test_moderators_list_renders_with_custom_user_moderator(admin_client, other_user):
    Moderator.objects.create(user=other_user)
    response = admin_client.get(moderators_list)
    assert_contains(response, other_user.username)
