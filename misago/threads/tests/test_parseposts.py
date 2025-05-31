from io import StringIO

from django.core import management

from ..management.commands import parseposts


def call_command():
    command = parseposts.Command()

    out = StringIO()
    management.call_command(command, stdout=out)
    return tuple(l.strip() for l in out.getvalue().strip().splitlines())


def test_parseposts_command_does_nothing_if_there_are_no_posts(db):
    command_output = call_command()
    assert command_output == ("No posts were found",)


def test_parseposts_command_reparses_existing_posts(post):
    post.original = "Hello **world**!"
    post.metadata = {"outdated": True}
    post.save()

    call_command()

    post.refresh_from_db()
    assert post.parsed == "<p>Hello <strong>world</strong>!</p>"
    assert post.metadata == {}
