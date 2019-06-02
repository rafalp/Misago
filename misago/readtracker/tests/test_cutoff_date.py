from datetime import timedelta
from unittest.mock import Mock

from django.utils import timezone

from ...conf.test import override_dynamic_settings
from ..cutoffdate import get_cutoff_date


def test_cutoff_date_for_no_user_is_calculated_from_setting(dynamic_settings):
    cutoff_date = get_cutoff_date(dynamic_settings)
    valid_cutoff_date = timezone.now() - timedelta(
        days=dynamic_settings.readtracker_cutoff
    )
    assert cutoff_date < valid_cutoff_date


def test_cutoff_date_for_recently_joined_user_is_their_join_date(dynamic_settings):
    user = Mock(is_authenticated=True, joined_on=timezone.now())
    cutoff_date = get_cutoff_date(dynamic_settings, user)
    assert cutoff_date == user.joined_on


@override_dynamic_settings(readtracker_cutoff=5)
def test_cutoff_date_for_old_user_is_calculated_from_setting(dynamic_settings):
    user = Mock(is_authenticated=True, joined_on=timezone.now() - timedelta(days=6))
    cutoff_date = get_cutoff_date(dynamic_settings, user)
    valid_cutoff_date = timezone.now() - timedelta(
        days=dynamic_settings.readtracker_cutoff
    )
    assert cutoff_date < valid_cutoff_date
    assert cutoff_date > user.joined_on


def test_cutoff_date_for_anonymous_user_is_calculated_from_setting(dynamic_settings):
    user = Mock(is_authenticated=False)
    cutoff_date = get_cutoff_date(dynamic_settings, user)
    valid_cutoff_date = timezone.now() - timedelta(
        days=dynamic_settings.readtracker_cutoff
    )
    assert cutoff_date < valid_cutoff_date
