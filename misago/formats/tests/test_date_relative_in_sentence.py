from datetime import timedelta

from django.utils import timezone
from freezegun import freeze_time

from ..daterelative import date_relative_in_sentence


def test_date_relative_in_sentence_formats_recent_date():
    assert date_relative_in_sentence(timezone.now()) == "a moment ago"


def test_date_relative_in_sentence_formats_date_few_seconds_ago():
    timestamp = timezone.now() - timedelta(seconds=5)
    assert date_relative_in_sentence(timestamp) == "a moment ago"


def test_date_relative_in_sentence_formats_date_few_seconds_in_future():
    timestamp = timezone.now() + timedelta(seconds=5)
    assert date_relative_in_sentence(timestamp) == "a moment ago"


def test_date_relative_in_sentence_formats_date_few_minutes_ago():
    timestamp = timezone.now() - timedelta(minutes=5)
    assert date_relative_in_sentence(timestamp) == "5 minutes ago"


def test_date_relative_in_sentence_formats_date_few_minutes_in_future():
    timestamp = timezone.now() + timedelta(minutes=5)
    assert date_relative_in_sentence(timestamp) == "in 5 minutes"


def test_date_relative_in_sentence_formats_date_few_hours_ago():
    timestamp = timezone.now() - timedelta(hours=2)
    assert date_relative_in_sentence(timestamp) == "2 hours ago"


def test_date_relative_in_sentence_formats_date_few_hours_in_future():
    timestamp = timezone.now() + timedelta(hours=2)
    assert date_relative_in_sentence(timestamp) == "in 2 hours"


@freeze_time("2024-07-27 21:37")
def test_date_relative_in_sentence_formats_date_today():
    timestamp = timezone.now() - timedelta(hours=7)
    assert date_relative_in_sentence(timestamp) == "at 2:37 PM"


@freeze_time("2024-07-27 11:37")
def test_date_relative_in_sentence_formats_date_today_in_future():
    timestamp = timezone.now() + timedelta(hours=7)
    assert date_relative_in_sentence(timestamp) == "today at 6:37 PM"


@freeze_time("2024-07-27 15:12")
def test_date_relative_in_sentence_formats_date_yesterday():
    timestamp = timezone.now() - timedelta(hours=24)
    assert date_relative_in_sentence(timestamp) == "yesterday at 3:12 PM"


@freeze_time("2024-07-27 15:12")
def test_date_relative_in_sentence_formats_date_tomorrow():
    timestamp = timezone.now() + timedelta(hours=24)
    assert date_relative_in_sentence(timestamp) == "tomorrow at 3:12 PM"


@freeze_time("2024-07-27 15:12")
def test_date_relative_in_sentence_formats_date_few_days_ago():
    timestamp = timezone.now() - timedelta(hours=72)
    assert date_relative_in_sentence(timestamp) == "Wednesday at 3:12 PM"


@freeze_time("2024-07-23 00:00")
def test_date_relative_in_sentence_uses_hours_instead_of_midnight():
    timestamp = timezone.now() - timedelta(hours=24)
    assert date_relative_in_sentence(timestamp) == "yesterday at 12:00 AM"


@freeze_time("2024-07-23 00:00")
def test_date_relative_in_sentence_uses_day_and_month_for_past_date_this_year():
    timestamp = timezone.now() - timedelta(days=100)
    assert date_relative_in_sentence(timestamp) == "April 14"


@freeze_time("2024-07-23 00:00")
def test_date_relative_in_sentence_uses_day_and_month_for_future_date_this_year():
    timestamp = timezone.now() + timedelta(days=100)
    assert date_relative_in_sentence(timestamp) == "October 31"


@freeze_time("2024-07-23 00:00")
def test_date_relative_in_sentence_uses_day_and_month_for_date_previous_year():
    timestamp = timezone.now() - timedelta(days=400)
    assert date_relative_in_sentence(timestamp) == "June 19, 2023"


@freeze_time("2024-07-23 00:00")
def test_date_relative_in_sentence_uses_day_and_month_for_date_next_year():
    timestamp = timezone.now() + timedelta(days=400)
    assert date_relative_in_sentence(timestamp) == "August 27, 2025"
