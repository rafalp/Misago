from io import StringIO

import pytest
from django.core import management

from ..management.commands import synchronizethreads


def call_command():
    command = synchronizethreads.Command()

    out = StringIO()
    management.call_command(command, stdout=out)
    return tuple(l.strip() for l in out.getvalue().strip().splitlines())


def test_synchronizethreads_command_does_nothing_if_there_are_no_threads(db):
    with pytest.raises(management.CommandError) as exc_info:
        command_output = call_command()

    assert exc_info.value.args == ("No threads exist.",)


def test_synchronizethreads_command_synchronizes_threads(
    thread_factory, default_category
):
    thread_factory(default_category)
    thread_factory(default_category)

    command_output = call_command()

    assert command_output[-1] == "Synchronized 2 threads."
