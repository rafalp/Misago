from ..enums import CUSTOM_GROUP_ID_START
from ..models import Group


def test_admins_group_is_only_group_with_admin_status(
    admins_group, moderators_group, members_group, guests_group
):
    assert admins_group.is_admin
    assert not moderators_group.is_admin
    assert not members_group.is_admin
    assert not guests_group.is_admin


def test_custom_group_is_not_admin(db):
    group = Group.objects.create(name="Custom", slug="custom")
    assert not group.is_admin


def test_standard_groups_are_protected(
    admins_group, moderators_group, members_group, guests_group
):
    assert admins_group.is_protected
    assert moderators_group.is_protected
    assert members_group.is_protected
    assert guests_group.is_protected


def test_custom_group_is_not_protected(db):
    group = Group.objects.create(name="Custom", slug="custom")
    assert not group.is_protected


def test_custom_group_id_is_greater_than_default_groups_ids(db):
    group = Group.objects.create(name="Custom", slug="custom")
    assert group.id >= CUSTOM_GROUP_ID_START
