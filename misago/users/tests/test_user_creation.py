import pytest
from django.contrib.auth import get_user_model

from ...permissions.permissionsid import get_permissions_id
from ..enums import DefaultGroupId
from ..models import Rank
from ..utils import hash_email

User = get_user_model()


def test_user_is_created(db):
    user = User.objects.create_user("User", "test@example.com")
    assert user.pk
    assert user.joined_on

    assert not user.is_staff
    assert not user.is_superuser
    assert not user.is_misago_root


def test_user_is_created_with_username_and_slug(db):
    user = User.objects.create_user("UserName", "test@example.com")
    assert user.slug == "username"


def test_user_is_created_with_normalized_email_and_email_hash(db):
    user = User.objects.create_user("User", "test@eXamPLe.com")
    assert user.email == "test@example.com"
    assert user.email_hash == hash_email(user.email)


def test_user_is_created_with_online_tracker(db):
    user = User.objects.create_user("User", "test@example.com")
    assert user.online_tracker
    assert user.online_tracker.last_click == user.last_login


def test_user_is_created_with_useable_password(db):
    password = "password"
    user = User.objects.create_user("UserUserame", "test@example.com", password)
    assert user.check_password(password)


def test_user_is_created_with_default_rank(db):
    user = User.objects.create_user("User", "test@example.com")
    assert user.rank == Rank.objects.get_default()


def test_user_is_created_with_custom_rank(db):
    rank = Rank.objects.create(name="Test rank")
    user = User.objects.create_user("User", "test@example.com", rank=rank)
    assert user.rank == rank


def test_user_is_created_with_default_group(db):
    user = User.objects.create_user("User", "test@example.com")
    assert user.group_id == DefaultGroupId.MEMBERS.value
    assert user.groups_ids == [DefaultGroupId.MEMBERS.value]
    assert user.permissions_id == get_permissions_id(user.groups_ids)


def test_user_is_created_with_custom_group(db, moderators_group):
    user = User.objects.create_user("User", "test@example.com", group=moderators_group)
    assert user.group_id == moderators_group.id
    assert user.groups_ids == [moderators_group.id]
    assert user.permissions_id == get_permissions_id(user.groups_ids)


def test_user_is_created_with_custom_group_id(db, moderators_group):
    user = User.objects.create_user(
        "User", "test@example.com", group_id=moderators_group.id
    )
    assert user.group_id == moderators_group.id
    assert user.groups_ids == [moderators_group.id]
    assert user.permissions_id == get_permissions_id(user.groups_ids)


def test_user_is_created_with_secondary_group(db, moderators_group):
    user = User.objects.create_user(
        "User",
        "test@example.com",
        secondary_groups=[moderators_group],
    )
    assert user.group_id == DefaultGroupId.MEMBERS.value
    assert user.groups_ids == [moderators_group.id, DefaultGroupId.MEMBERS.value]
    assert user.permissions_id == get_permissions_id(user.groups_ids)


def test_user_is_created_with_secondary_group_id(db, moderators_group):
    user = User.objects.create_user(
        "User",
        "test@example.com",
        secondary_groups_ids=[moderators_group.id],
    )
    assert user.group_id == DefaultGroupId.MEMBERS.value
    assert user.groups_ids == [moderators_group.id, DefaultGroupId.MEMBERS.value]
    assert user.permissions_id == get_permissions_id(user.groups_ids)


def test_user_is_created_with_secondary_groups(db, admins_group, moderators_group):
    user = User.objects.create_user(
        "User",
        "test@example.com",
        secondary_groups=[admins_group, moderators_group],
    )
    assert user.group_id == DefaultGroupId.MEMBERS.value
    assert user.groups_ids == [
        admins_group.id,
        moderators_group.id,
        DefaultGroupId.MEMBERS.value,
    ]
    assert user.permissions_id == get_permissions_id(user.groups_ids)


def test_user_is_created_with_secondary_groups_ids(db, admins_group, moderators_group):
    user = User.objects.create_user(
        "User",
        "test@example.com",
        secondary_groups_ids=[admins_group.id, moderators_group.id],
    )
    assert user.group_id == DefaultGroupId.MEMBERS.value
    assert user.groups_ids == [
        admins_group.id,
        moderators_group.id,
        DefaultGroupId.MEMBERS.value,
    ]
    assert user.permissions_id == get_permissions_id(user.groups_ids)


def test_newly_created_user_last_login_is_same_as_join_date(db):
    user = User.objects.create_user("User", "test@example.com")
    assert user.last_login == user.joined_on


def test_user_is_created_with_authenticated_role(db):
    user = User.objects.create_user("User", "test@example.com")
    assert user.roles.get(special_role="authenticated")


def test_user_is_created_with_diacritics_in_email(db):
    email = "łóć@łexąmple.com"
    user = User.objects.create_user("UserName", email)
    assert user.email == email


def test_creating_user_without_username_raises_value_error(db):
    with pytest.raises(ValueError):
        User.objects.create_user("", "test@example.com")


def test_creating_user_without_email_raises_value_error(db):
    with pytest.raises(ValueError):
        User.objects.create_user("User", "")


def test_creating_user_with_group_and_group_id_raises_value_error(
    db, admins_group, moderators_group
):
    with pytest.raises(ValueError):
        User.objects.create_user(
            "User",
            "test@example.com",
            group=admins_group,
            group_id=moderators_group.id,
        )


def test_creating_user_with_secondary_groups_and_secondary_groups_ids_raises_value_error(
    db, admins_group, moderators_group
):
    with pytest.raises(ValueError):
        User.objects.create_user(
            "User",
            "test@example.com",
            secondary_groups=[admins_group],
            secondary_groups_ids=[moderators_group.id],
        )


def test_creating_user_with_groups_id_raises_value_error(db):
    with pytest.raises(ValueError):
        User.objects.create_user(
            "User",
            "test@example.com",
            groups_id=[1, 2, 3],
        )


def test_creating_user_with_permissions_id_raises_value_error(db):
    with pytest.raises(ValueError):
        User.objects.create_user(
            "User",
            "test@example.com",
            permissions_id="error",
        )


def test_create_superuser(db):
    user = User.objects.create_superuser("User", "test@example.com")
    assert user.is_staff
    assert user.is_superuser
    assert user.is_misago_root


def test_superuser_is_created_with_team_rank(db):
    user = User.objects.create_superuser("User", "test@example.com")
    assert "team" in str(user.rank)


def test_superuser_is_created_with_admins_group(db, admins_group):
    user = User.objects.create_superuser("User", "test@example.com")
    assert user.group_id == admins_group.id
    assert user.groups_ids == [admins_group.id]
    assert user.permissions_id == get_permissions_id(user.groups_ids)


def test_creating_superuser_without_staff_status_raises_value_error(db):
    with pytest.raises(ValueError):
        User.objects.create_superuser("User", "test@example.com", is_staff=False)


def test_creating_superuser_without_superuser_status_raises_value_error(db):
    with pytest.raises(ValueError):
        User.objects.create_superuser("User", "test@example.com", is_superuser=False)
