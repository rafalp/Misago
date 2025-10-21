from datetime import timedelta
from io import StringIO

import pytest
from django.core import management
from django.utils import timezone

from ...threads.models import Thread
from ..management.commands import prunecategories
from ..models import Category


def call_command():
    command = prunecategories.Command()

    out = StringIO()
    management.call_command(command, stdout=out)
    return tuple(l.strip() for l in out.getvalue().strip().splitlines())


def test_prunecategories_command_ignores_category_without_pruning(default_category):
    command_output = call_command()
    assert command_output[0].strip() == "Pruned categories: 0"


def test_prunecategories_command_ignores_empty_category(default_category):
    default_category.prune_started_after = 20
    default_category.save()

    command_output = call_command()
    assert command_output[0].strip() == "Pruned categories: 1"
    assert default_category.name in command_output[-1].strip()


def test_prunecategories_command_prunes_threads_using_start_date(
    thread_factory, thread_reply_factory, default_category, day_seconds
):
    default_category.prune_started_after = 3
    default_category.save()

    old_thread = thread_factory(default_category, started_at=day_seconds * -4)
    old_thread_with_reply = thread_factory(
        default_category, started_at=day_seconds * -4
    )
    thread_reply_factory(old_thread_with_reply)

    recent_thread = thread_factory(default_category, started_at=day_seconds * -2)

    command_output = call_command()
    assert command_output[0].strip() == "Pruned categories: 1"

    with pytest.raises(Thread.DoesNotExist):
        old_thread.refresh_from_db()

    with pytest.raises(Thread.DoesNotExist):
        old_thread_with_reply.refresh_from_db()

    recent_thread.refresh_from_db()


def test_prunecategories_command_archives_threads_using_start_date(
    thread_factory,
    thread_reply_factory,
    default_category,
    sibling_category,
    day_seconds,
):
    default_category.archive_pruned_in = sibling_category
    default_category.prune_started_after = 3
    default_category.save()

    old_thread = thread_factory(default_category, started_at=day_seconds * -4)
    old_thread_with_reply = thread_factory(
        default_category, started_at=day_seconds * -4
    )
    old_thread_reply = thread_reply_factory(old_thread_with_reply)

    recent_thread = thread_factory(default_category, started_at=day_seconds * -2)

    command_output = call_command()
    assert command_output[0].strip() == "Pruned categories: 1"

    old_thread.refresh_from_db()
    assert old_thread.category == sibling_category

    old_thread_with_reply.refresh_from_db()
    assert old_thread_with_reply.category == sibling_category

    old_thread_reply.refresh_from_db()
    assert old_thread_reply.category == sibling_category

    recent_thread.refresh_from_db()
    assert recent_thread.category == default_category


def test_prunecategories_command_prunes_threads_using_last_reply_date(
    thread_factory, thread_reply_factory, default_category, day_seconds
):
    default_category.prune_replied_after = 10
    default_category.save()

    old_thread = thread_factory(default_category, started_at=day_seconds * -15)
    old_thread_with_old_reply = thread_factory(
        default_category, started_at=day_seconds * -14
    )
    old_thread_with_recent_reply = thread_factory(
        default_category, started_at=day_seconds * -13
    )

    thread_reply_factory(old_thread_with_old_reply, posted_at=day_seconds * -12)
    thread_reply_factory(old_thread_with_recent_reply, posted_at=day_seconds * -8)

    recent_thread = thread_factory(default_category, started_at=day_seconds * -2)
    recent_thread_with_recent_reply = thread_factory(default_category)

    thread_reply_factory(recent_thread_with_recent_reply)

    command_output = call_command()
    assert command_output[0].strip() == "Pruned categories: 1"

    with pytest.raises(Thread.DoesNotExist):
        old_thread.refresh_from_db()

    with pytest.raises(Thread.DoesNotExist):
        old_thread_with_old_reply.refresh_from_db()

    old_thread_with_recent_reply.refresh_from_db()
    recent_thread_with_recent_reply.refresh_from_db()
    recent_thread.refresh_from_db()


def test_prunecategories_command_archives_threads_using_last_reply_date(
    thread_factory,
    thread_reply_factory,
    default_category,
    sibling_category,
    day_seconds,
):
    default_category.archive_pruned_in = sibling_category
    default_category.prune_replied_after = 10
    default_category.save()

    old_thread = thread_factory(default_category, started_at=day_seconds * -15)
    old_thread_with_old_reply = thread_factory(
        default_category, started_at=day_seconds * -14
    )
    old_thread_with_recent_reply = thread_factory(
        default_category, started_at=day_seconds * -13
    )

    old_thread_old_reply = thread_reply_factory(
        old_thread_with_old_reply, posted_at=day_seconds * -12
    )
    old_thread_recent_reply = thread_reply_factory(
        old_thread_with_recent_reply, posted_at=day_seconds * -8
    )

    recent_thread = thread_factory(default_category, started_at=day_seconds * -2)
    recent_thread_with_recent_reply = thread_factory(default_category)

    recent_thread_recent_reply = thread_reply_factory(recent_thread_with_recent_reply)

    command_output = call_command()
    assert command_output[0].strip() == "Pruned categories: 1"

    old_thread.refresh_from_db()
    assert old_thread.category == sibling_category

    old_thread_with_old_reply.refresh_from_db()
    assert old_thread_with_old_reply.category == sibling_category

    old_thread_old_reply.refresh_from_db()
    assert old_thread_old_reply.category == sibling_category

    old_thread_with_recent_reply.refresh_from_db()
    assert old_thread_with_recent_reply.category == default_category

    old_thread_recent_reply.refresh_from_db()
    assert old_thread_recent_reply.category == default_category

    recent_thread_with_recent_reply.refresh_from_db()
    assert recent_thread.category == default_category

    recent_thread_recent_reply.refresh_from_db()
    assert recent_thread_recent_reply.category == default_category

    recent_thread.refresh_from_db()
    assert recent_thread.category == default_category
