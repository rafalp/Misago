from datetime import timedelta
from io import StringIO

import pytest
from django.core import management
from django.core.management.base import CommandError

from ..logging import log_search
from ..management.commands import clearsearchlogs
from ..models import SearchLog


def call_command(*args):
    command = clearsearchlogs.Command()
    stdout = StringIO()

    management.call_command(command, *args, stdout=stdout)

    return tuple(l.strip() for l in stdout.getvalue().strip().splitlines())


def test_clearsearchlogs_command_clears_old_logs(mocker, user):
    log_search(user, "127.0.0.1", "example search", is_public=True)
    log_search(None, "127.0.0.1", "example search")
    log_search(user, "127.0.0.1", "example search", is_public=True)
    log_search(None, "127.0.0.1", "example search")

    for i, log in enumerate(SearchLog.objects.all()[:3]):
        log.searched_at -= timedelta(days=50 + i)
        log.save()

    interactive = mocker.patch(
        "misago.search.management.commands.clearsearchlogs.input", return_value="yes"
    )

    stdout = call_command()

    assert stdout == ("Deleted 3 search logs in 0.00s.",)

    interactive.assert_called_once_with(
        "This will DELETE search logs older than 45 days!"
        "\n"
        "Are you sure you want to do this?"
        "\n\n"
        "Type 'yes' to continue, or 'no' to cancel: ",
    )

    assert SearchLog.objects.count() == 1


def test_clearsearchlogs_command_clears_old_logs_without_input(mocker, user):
    log_search(user, "127.0.0.1", "example search", is_public=True)
    log_search(None, "127.0.0.1", "example search")
    log_search(user, "127.0.0.1", "example search", is_public=True)
    log_search(None, "127.0.0.1", "example search")

    for i, log in enumerate(SearchLog.objects.all()[:3]):
        log.searched_at -= timedelta(days=50 + i)
        log.save()

    interactive = mocker.patch(
        "misago.search.management.commands.clearsearchlogs.input", return_value="yes"
    )

    stdout = call_command("--noinput")

    assert stdout == ("Deleted 3 search logs in 0.00s.",)

    interactive.assert_not_called()

    assert SearchLog.objects.count() == 1


def test_clearsearchlogs_command_cancels_old_logs_clear(mocker, user):
    log_search(user, "127.0.0.1", "example search", is_public=True)
    log_search(None, "127.0.0.1", "example search")
    log_search(user, "127.0.0.1", "example search", is_public=True)
    log_search(None, "127.0.0.1", "example search")

    for i, log in enumerate(SearchLog.objects.all()[:3]):
        log.searched_at -= timedelta(days=50 + i)
        log.save()

    interactive = mocker.patch(
        "misago.search.management.commands.clearsearchlogs.input", return_value="no"
    )

    with pytest.raises(CommandError) as exc_info:
        call_command()

    assert str(exc_info.value) == "Deleting old search logs cancelled."

    interactive.assert_called_once_with(
        "This will DELETE search logs older than 45 days!"
        "\n"
        "Are you sure you want to do this?"
        "\n\n"
        "Type 'yes' to continue, or 'no' to cancel: ",
    )

    assert SearchLog.objects.count() == 4


def test_clearsearchlogs_command_clears_all_logs(mocker, user):
    log_search(user, "127.0.0.1", "example search", is_public=True)
    log_search(None, "127.0.0.1", "example search")
    log_search(user, "127.0.0.1", "example search", is_public=True)
    log_search(None, "127.0.0.1", "example search")

    for i, log in enumerate(SearchLog.objects.all()[:3]):
        log.searched_at -= timedelta(days=50 + i)
        log.save()

    interactive = mocker.patch(
        "misago.search.management.commands.clearsearchlogs.input", return_value="yes"
    )

    stdout = call_command("--all")

    assert stdout == ("Deleted 4 search logs in 0.00s.",)

    interactive.assert_called_once_with(
        "This will DELETE ALL search logs!"
        "\n"
        "Are you sure you want to do this?"
        "\n\n"
        "Type 'yes' to continue, or 'no' to cancel: ",
    )

    assert not SearchLog.objects.exists()


def test_clearsearchlogs_command_clears_all_logs_without_input(mocker, user):
    log_search(user, "127.0.0.1", "example search", is_public=True)
    log_search(None, "127.0.0.1", "example search")
    log_search(user, "127.0.0.1", "example search", is_public=True)
    log_search(None, "127.0.0.1", "example search")

    for i, log in enumerate(SearchLog.objects.all()[:3]):
        log.searched_at -= timedelta(days=50 + i)
        log.save()

    interactive = mocker.patch(
        "misago.search.management.commands.clearsearchlogs.input", return_value="yes"
    )

    stdout = call_command("--all", "--noinput")

    assert stdout == ("Deleted 4 search logs in 0.00s.",)

    interactive.assert_not_called()

    assert not SearchLog.objects.exists()


def test_clearsearchlogs_command_cancels_all_logs_clear(mocker, user):
    log_search(user, "127.0.0.1", "example search", is_public=True)
    log_search(None, "127.0.0.1", "example search")
    log_search(user, "127.0.0.1", "example search", is_public=True)
    log_search(None, "127.0.0.1", "example search")

    for i, log in enumerate(SearchLog.objects.all()[:3]):
        log.searched_at -= timedelta(days=50 + i)
        log.save()

    interactive = mocker.patch(
        "misago.search.management.commands.clearsearchlogs.input", return_value="no"
    )

    with pytest.raises(CommandError) as exc_info:
        call_command("--all")

    assert str(exc_info.value) == "Deleting all search logs cancelled."

    interactive.assert_called_once_with(
        "This will DELETE ALL search logs!"
        "\n"
        "Are you sure you want to do this?"
        "\n\n"
        "Type 'yes' to continue, or 'no' to cancel: ",
    )

    assert SearchLog.objects.count() == 4
