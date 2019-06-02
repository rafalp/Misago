from datetime import timedelta
from io import StringIO

from django.core import management
from django.utils import timezone

from ...conf.test import override_dynamic_settings
from ..management.commands import clearreadtracker
from ..models import PostRead


def call_command():
    command = clearreadtracker.Command()

    out = StringIO()
    management.call_command(command, stdout=out)
    return out.getvalue().strip().splitlines()[-1].strip()


def test_command_works_if_there_are_no_read_tracker_entries(db):
    command_output = call_command()
    assert command_output == "No expired entries were found"


@override_dynamic_settings(readtracker_cutoff=5)
def test_recent_read_tracker_entry_is_not_cleared(user, post):
    existing = PostRead.objects.create(
        user=user,
        category=post.category,
        thread=post.thread,
        post=post,
        last_read_on=timezone.now(),
    )

    command_output = call_command()
    assert command_output == "No expired entries were found"
    assert PostRead.objects.exists()


@override_dynamic_settings(readtracker_cutoff=5)
def test_old_read_tracker_entry_is_cleared(user, post):
    existing = PostRead.objects.create(
        user=user,
        category=post.category,
        thread=post.thread,
        post=post,
        last_read_on=timezone.now() - timedelta(days=10),
    )

    command_output = call_command()
    assert command_output == "Deleted 1 expired entries"
    assert not PostRead.objects.exists()
