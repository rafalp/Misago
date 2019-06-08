from datetime import timedelta
from io import StringIO

import pytest
from django.core.management import call_command
from django.utils import timezone

from ...conf.test import override_dynamic_settings
from ..management.commands import removeoldips

IP_STORE_TIME = 2


@pytest.fixture
def user_with_ip(user):
    user.joined_from_ip = "127.0.0.1"
    user.save()
    return user


@pytest.fixture
def user_with_old_ip(user_with_ip):
    joined_on_past = timezone.now() - timedelta(days=IP_STORE_TIME + 1)
    user_with_ip.joined_on = joined_on_past
    user_with_ip.save()
    return user_with_ip


def test_recent_user_joined_ip_is_not_removed_by_command(user_with_ip):
    call_command(removeoldips.Command(), stdout=StringIO())
    user_with_ip.refresh_from_db()
    assert user_with_ip.joined_from_ip


@override_dynamic_settings(ip_storage_time=IP_STORE_TIME)
def test_old_user_joined_ip_is_removed_by_command(user_with_old_ip):
    call_command(removeoldips.Command(), stdout=StringIO())
    user_with_old_ip.refresh_from_db()
    assert user_with_old_ip.joined_from_ip is None


@override_dynamic_settings(ip_storage_time=None)
def test_old_user_joined_ip_is_not_removed_by_command_if_removal_is_disabled(
    user_with_old_ip
):
    call_command(removeoldips.Command(), stdout=StringIO())
    user_with_old_ip.refresh_from_db()
    assert user_with_old_ip.joined_from_ip


@override_dynamic_settings(ip_storage_time=IP_STORE_TIME)
def test_command_displays_message_if_old_ip_removal_is_enabled(db):
    stdout = StringIO()
    call_command(removeoldips.Command(), stdout=stdout)

    command_output = stdout.getvalue().splitlines()[0].strip()
    assert command_output == "IP addresses older than 2 days have been removed."


@override_dynamic_settings(ip_storage_time=None)
def test_command_displays_message_if_old_ip_removal_is_disabled(db):
    stdout = StringIO()
    call_command(removeoldips.Command(), stdout=stdout)

    command_output = stdout.getvalue().splitlines()[0].strip()
    assert command_output == "Old IP removal is disabled."
