from io import StringIO

from django.core import management

from ..exceptions import SearchBackendError
from ..management.commands import initializesearch


def call_command():
    command = initializesearch.Command()

    stdout = StringIO()
    stderr = StringIO()

    management.call_command(command, stdout=stdout, stderr=stderr)
    return (
        tuple(l.strip() for l in stdout.getvalue().strip().splitlines()),
        tuple(l.strip() for l in stderr.getvalue().strip().splitlines()),
    )


def test_initializesearch_command_initializes_search_backend():
    stdout, stderr = call_command()

    assert stdout[-1] == ("Initialized the search backend: PostgreSQL full-text search")
    assert not stderr


def test_initializesearch_command_prints_initialization_error(mocker):
    mocker.patch(
        "misago.search.posts.posts_search.backend.initialize",
        side_effect=SearchBackendError("This backend is not available."),
    )

    stdout, stderr = call_command()

    assert stderr == (
        'Error initializing the search backend "PostgreSQL full-text search":',
        "",
        "This backend is not available.",
    )
    assert not stdout
