from io import StringIO

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from ...conf.test import override_dynamic_settings
from ..management.commands import deletemarkedusers
from ..models import DeletedUser
from ..test import create_test_user

User = get_user_model()


def call_deletemarkedusers():
    out = StringIO()
    call_command(deletemarkedusers.Command(), stdout=out)
    return out.getvalue().splitlines()[0].strip()


@pytest.fixture
def user_marked_for_delete(user):
    user.mark_for_delete()
    return user


def test_deletemarkedusers_command_deletes_marked_user(user_marked_for_delete):
    output = call_deletemarkedusers()
    assert output == "Deleted users: 1"

    with pytest.raises(User.DoesNotExist):
        user_marked_for_delete.refresh_from_db()


def test_deletemarkedusers_command_records_user_deletion(user_marked_for_delete):
    output = call_deletemarkedusers()
    assert output == "Deleted users: 1"

    DeletedUser.objects.get(deleted_by=DeletedUser.DELETED_BY_SELF)


@override_dynamic_settings(allow_delete_own_account=False)
def test_deletemarkedusers_command_ignores_delete_own_account_setting_change(
    user_marked_for_delete,
):
    output = call_deletemarkedusers()
    assert output == "Deleted users: 1"

    with pytest.raises(User.DoesNotExist):
        user_marked_for_delete.refresh_from_db()


def test_deletemarkedusers_command_excludes_users_not_marked_for_deletion(user):
    output = call_deletemarkedusers()
    assert output == "Deleted users: 0"

    user.refresh_from_db()


def test_deletemarkedusers_command_excludes_staff_users(user_marked_for_delete):
    """staff users are extempt from deletion"""
    user_marked_for_delete.is_staff = True
    user_marked_for_delete.save()

    output = call_deletemarkedusers()
    assert output == "Deleted users: 0"

    user_marked_for_delete.refresh_from_db()


def test_deletemarkedusers_command_excludes_admins(
    user_marked_for_delete, admins_group
):
    """staff users are extempt from deletion"""
    user_marked_for_delete.set_groups(admins_group)
    user_marked_for_delete.save()

    output = call_deletemarkedusers()
    assert output == "Deleted users: 0"

    user_marked_for_delete.refresh_from_db()


def test_deletemarkedusers_command_excludes_root_admins(user_marked_for_delete):
    """staff users are extempt from deletion"""
    user_marked_for_delete.is_misago_root = True
    user_marked_for_delete.save()

    output = call_deletemarkedusers()
    assert output == "Deleted users: 0"

    user_marked_for_delete.refresh_from_db()
