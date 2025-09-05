from io import StringIO

import pytest
from django.core import management

from ..management.commands import parseposts


def call_command():
    command = parseposts.Command()

    out = StringIO()
    management.call_command(command, stdout=out)
    return tuple(l.strip() for l in out.getvalue().strip().splitlines())


def test_parseposts_command_does_nothing_if_there_are_no_posts(db):
    with pytest.raises(management.CommandError) as exc_info:
        command_output = call_command()

    assert exc_info.value.args == ("No posts exist.",)


def test_parseposts_command_reparses_existing_posts(post):
    post.original = "Hello **world**!"
    post.metadata = {"outdated": True}
    post.save()

    command_output = call_command()

    assert command_output[-1] == "Parsed one post."

    post.refresh_from_db()
    assert post.parsed == "<p>Hello <strong>world</strong>!</p>"
    assert post.metadata == {}
