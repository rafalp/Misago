from datetime import timedelta

from django.utils import timezone
from freezegun import freeze_time

from ..daterelative import date_relative_short


def test_date_relative_short_formats_recent_date():
    assert date_relative_short(timezone.now()) == "now"


def test_date_relative_short_formats_date_few_minutes_ago():
    timestamp = timezone.now() - timedelta(minutes=5)
    assert date_relative_short(timestamp) == "5m"


def test_date_relative_short_formats_date_few_hours_ago():
    timestamp = timezone.now() - timedelta(hours=5)
    assert date_relative_short(timestamp) == "5h"


def test_date_relative_short_formats_date_few_days_ago():
    timestamp = timezone.now() - timedelta(hours=5 * 24)
    assert date_relative_short(timestamp) == "5d"


@freeze_time("2024-07-27 15:12")
def test_date_relative_short_formats_date_from_this_year():
    timestamp = timezone.now() - timedelta(days=100)
    assert date_relative_short(timestamp) == "Apr 18"


@freeze_time("2024-07-27 15:12")
def test_date_relative_short_formats_date_from_other_year():
    timestamp = timezone.now() - timedelta(days=400)
    assert date_relative_short(timestamp) == "Jun 2023"
