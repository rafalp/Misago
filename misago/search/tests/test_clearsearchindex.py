from io import StringIO

from django.core import management

from ..exceptions import SearchBackendError
from ..management.commands import clearsearchindex


def call_command():
    command = clearsearchindex.Command()

    stdout = StringIO()
    stderr = StringIO()

    management.call_command(command, stdout=stdout, stderr=stderr)
    return (
        tuple(l.strip() for l in stdout.getvalue().strip().splitlines()),
        tuple(l.strip() for l in stderr.getvalue().strip().splitlines()),
    )


def test_clearsearchindex_command_clears_search_index(db):
    stdout, stderr = call_command()

    assert stdout == (
        'Cleared the search index using the "PostgreSQL full-text search" backend.',
        "",
        "Time: 0.00s",
    )
    assert not stderr


def test_clearsearchindex_command_prints_backend_error(mocker):
    mocker.patch(
        "misago.search.posts.posts_search.backend.clear",
        side_effect=SearchBackendError("This backend is not available."),
    )

    stdout, stderr = call_command()

    assert stderr == (
        'Error clearing the search index using the "PostgreSQL full-text search" backend:',
        "",
        "This backend is not available.",
    )
    assert not stdout
