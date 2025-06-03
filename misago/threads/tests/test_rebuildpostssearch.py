from io import StringIO

from django.core import management

from ..management.commands import rebuildpostssearch


def call_command():
    command = rebuildpostssearch.Command()

    out = StringIO()
    management.call_command(command, stdout=out)
    return tuple(l.strip() for l in out.getvalue().strip().splitlines())


def test_rebuildpostssearch_command_does_nothing_if_there_are_no_posts(db):
    command_output = call_command()
    assert command_output == ("No posts were found",)


def test_rebuildpostssearch_command_updates_existing_posts_search_documents(post):
    post.original = "Hello **world**!"
    post.save()

    call_command()

    post.refresh_from_db()
    assert post.search_document == "Test thread Hello world!"
