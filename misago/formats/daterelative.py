from datetime import datetime, timedelta
from math import floor

from django.utils import timezone
from django.utils.formats import date_format
from django.utils.translation import npgettext, pgettext


def date_relative(value: datetime) -> str:
    now = timezone.now()
    delta = abs((now - value).total_seconds())
    past = value < now

    if delta < 60:
        return pgettext("time ago", "moment ago")

    if delta < 60 * 47:
        minutes = round(delta / 60)
        if past:
            return npgettext(
                "minutes ago",
                "%(time)s minute ago",
                "%(time)s minutes ago",
                minutes,
            ) % {"time": minutes}

        return npgettext(
            "minutes in future",
            "In %(time)s minute",
            "In %(time)s minutes",
            minutes,
        ) % {"time": minutes}

    if delta < 3600 * 3:
        hours = round(delta / 3600)
        if past:
            return npgettext(
                "hours ago",
                "%(time)s hour ago",
                "%(time)s hours ago",
                hours,
            ) % {"time": hours}

        return npgettext(
            "hours in future",
            "In %(time)s hour",
            "In %(time)s hours",
            hours,
        ) % {"time": hours}

    if is_same_day(now, value):
        if past:
            return time_short(value)

        return pgettext("day at time", "Today at %(time)s") % {
            "time": time_short(value)
        }

    if is_yesterday(now, value):
        return pgettext("day at time", "Yesterday at %(time)s") % {
            "time": time_short(value)
        }

    if is_tomorrow(now, value):
        return pgettext("day at time", "Tomorrow at %(time)s") % {
            "time": time_short(value)
        }

    if past and delta < 3600 * 24 * 6:
        return pgettext("day at time", "%(day)s at %(time)s") % {
            "day": date_format(value, "l"),
            "time": time_short(value),
        }

    if is_same_year(now, value):
        return date_format(value, pgettext("same year date", "F j"))

    return date_format(value, pgettext("other year date", "F j, Y"))


def date_relative_in_sentence(value: datetime) -> str:
    now = timezone.now()
    delta = abs((now - value).total_seconds())
    past = value < now

    if delta < 60:
        return pgettext("time ago in sentence", "a moment ago")

    if delta < 60 * 47:
        minutes = round(delta / 60)
        if past:
            return npgettext(
                "minutes ago in sentence",
                "%(time)s minute ago",
                "%(time)s minutes ago",
                minutes,
            ) % {"time": minutes}

        return npgettext(
            "minutes in future in sentence",
            "in %(time)s minute",
            "in %(time)s minutes",
            minutes,
        ) % {"time": minutes}

    if delta < 3600 * 3:
        hours = round(delta / 3600)
        if past:
            return npgettext(
                "hours ago in sentence",
                "%(time)s hour ago",
                "%(time)s hours ago",
                hours,
            ) % {"time": hours}

        return npgettext(
            "hours in future in sentence",
            "in %(time)s hour",
            "in %(time)s hours",
            hours,
        ) % {"time": hours}

    if is_same_day(now, value):
        if past:
            return pgettext("day at time in sentence", "at %(time)s") % {
                "time": time_short(value)
            }

        return pgettext("day at time in sentence", "today at %(time)s") % {
            "time": time_short(value)
        }

    if is_yesterday(now, value):
        return pgettext("day at time in sentence", "yesterday at %(time)s") % {
            "time": time_short(value)
        }

    if is_tomorrow(now, value):
        return pgettext("day at time in sentence", "tomorrow at %(time)s") % {
            "time": time_short(value)
        }

    if past and delta < 3600 * 24 * 6:
        return pgettext("day at time in sentence", "%(day)s at %(time)s") % {
            "day": date_format(value, "l"),
            "time": time_short(value),
        }

    if is_same_year(now, value):
        return date_format(value, pgettext("same year date", "F j"))

    return date_format(value, pgettext("other year date", "F j, Y"))


def is_same_day(now: datetime, datetime_: datetime) -> bool:
    return date_format(now, "dmY") == date_format(datetime_, "dmY")


def is_yesterday(now: datetime, datetime_: datetime) -> bool:
    yesterday = now - timedelta(hours=24)
    return date_format(yesterday, "dmY") == date_format(datetime_, "dmY")


def is_tomorrow(now: datetime, datetime_: datetime) -> bool:
    yesterday = now + timedelta(hours=24)
    return date_format(yesterday, "dmY") == date_format(datetime_, "dmY")


def is_same_year(now: datetime, datetime_: datetime) -> bool:
    return date_format(now, "Y") == date_format(datetime_, "Y")


def date_relative_short(value: datetime) -> str:
    now = timezone.now()
    delta = abs((now - value).total_seconds())

    if delta < 60:
        return pgettext("time ago", "now")

    if delta < 60 * 55:
        minutes = round(delta / 60)
        return pgettext("short minutes", "%(time)sm") % {"time": minutes}

    if delta < 3600 * 24:
        hours = round(delta / 3600)
        return pgettext("short hours", "%(time)sh") % {"time": hours}

    if delta < 86400 * 7:
        days = round(delta / 86400)
        return pgettext("short days", "%(time)sd") % {"time": days}

    if now.year == value.year:
        return date_format(value, pgettext("short this year", "M j"))

    return date_format(value, pgettext("short other year", "M Y"))


def time_short(value: datetime) -> str:
    return date_format(
        value,
        pgettext("time short", "g:i A"),
        use_l10n=False,
    )
