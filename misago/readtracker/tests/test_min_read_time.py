from datetime import timedelta
from unittest.mock import Mock

from django.utils import timezone

from ...conf.test import override_dynamic_settings
from ..readtime import get_default_read_time


def test_default_read_time_for_empty_user_is_relative_to_current_time(dynamic_settings):
    default_read_time = get_default_read_time(dynamic_settings)
    valid_default_read_time = timezone.now() - timedelta(
        days=dynamic_settings.readtracker_cutoff
    )
    assert (valid_default_read_time - default_read_time).seconds < 1


def test_default_read_time_for_anonymous_user_is_relative_to_current_time(
    dynamic_settings, anonymous_user
):
    default_read_time = get_default_read_time(dynamic_settings, anonymous_user)
    valid_default_read_time = timezone.now() - timedelta(
        days=dynamic_settings.readtracker_cutoff
    )
    assert (valid_default_read_time - default_read_time).seconds < 1


def test_default_read_time_for_recently_registered_user_is_their_registration_date(
    dynamic_settings, user
):
    user = Mock(is_authenticated=True, joined_on=timezone.now())
    default_read_time = get_default_read_time(dynamic_settings, user)
    assert default_read_time == user.joined_on


@override_dynamic_settings(readtracker_cutoff=5)
def test_default_read_time_for_old_user_is_relative_to_current_time(dynamic_settings):
    user = Mock(is_authenticated=True, joined_on=timezone.now() - timedelta(days=6))
    default_read_time = get_default_read_time(dynamic_settings, user)
    valid_default_read_time = timezone.now() - timedelta(
        days=dynamic_settings.readtracker_cutoff
    )
    assert (valid_default_read_time - default_read_time).seconds < 1
    assert default_read_time > user.joined_on
