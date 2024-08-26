from datetime import timedelta
from io import StringIO

import pytest
from django.core import management
from django.utils import timezone

from ...conf.test import override_dynamic_settings
from ..management.commands import clearreadtracker
from ..models import ReadCategory, ReadThread


def call_command() -> list[str]:
    command = clearreadtracker.Command()

    out = StringIO()
    management.call_command(command, stdout=out)
    return [l.strip() for l in out.getvalue().strip().splitlines()]


def test_command_works_if_there_are_no_read_tracker_times(db):
    assert call_command() == [
        "Expired read times deleted:",
        "- Categories:   0",
        "- Threads:      0",
        "",
        "Remaining:",
        "- Categories:   0",
        "- Threads:      0",
    ]


@override_dynamic_settings(readtracker_cutoff=5)
def test_recent_category_read_time_is_not_cleared(user, default_category):
    read_time = ReadCategory.objects.create(
        user=user,
        category=default_category,
        read_time=timezone.now(),
    )

    assert call_command() == [
        "Expired read times deleted:",
        "- Categories:   0",
        "- Threads:      0",
        "",
        "Remaining:",
        "- Categories:   1",
        "- Threads:      0",
    ]

    read_time.refresh_from_db()


@override_dynamic_settings(readtracker_cutoff=5)
def test_old_category_read_time_is_cleared(user, default_category):
    read_time = ReadCategory.objects.create(
        user=user,
        category=default_category,
        read_time=timezone.now() - timedelta(days=10),
    )

    assert call_command() == [
        "Expired read times deleted:",
        "- Categories:   1",
        "- Threads:      0",
        "",
        "Remaining:",
        "- Categories:   0",
        "- Threads:      0",
    ]

    with pytest.raises(ReadCategory.DoesNotExist):
        read_time.refresh_from_db()


@override_dynamic_settings(readtracker_cutoff=5)
def test_recent_thread_read_time_is_not_cleared(user, default_category, thread):
    read_time = ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=thread,
        read_time=timezone.now(),
    )

    assert call_command() == [
        "Expired read times deleted:",
        "- Categories:   0",
        "- Threads:      0",
        "",
        "Remaining:",
        "- Categories:   0",
        "- Threads:      1",
    ]

    read_time.refresh_from_db()


@override_dynamic_settings(readtracker_cutoff=5)
def test_old_thread_read_time_is_cleared(user, default_category, thread):
    read_time = ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=thread,
        read_time=timezone.now() - timedelta(days=10),
    )

    assert call_command() == [
        "Expired read times deleted:",
        "- Categories:   0",
        "- Threads:      1",
        "",
        "Remaining:",
        "- Categories:   0",
        "- Threads:      0",
    ]

    with pytest.raises(ReadThread.DoesNotExist):
        read_time.refresh_from_db()
