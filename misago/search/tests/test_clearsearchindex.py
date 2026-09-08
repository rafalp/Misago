from io import StringIO

import pytest
from django.core import management

from ..exceptions import SearchBackendError
from ..management.commands import clearsearchindex
from ..models import PostSearch, ThreadSearch


def call_command():
    command = clearsearchindex.Command()

    stdout = StringIO()
    stderr = StringIO()

    management.call_command(command, stdout=stdout, stderr=stderr)
    return (
        tuple(l.strip() for l in stdout.getvalue().strip().splitlines()),
        tuple(l.strip() for l in stderr.getvalue().strip().splitlines()),
    )


def test_clearsearchindex_command_clears_search_index(thread, post):
    thread_search = ThreadSearch.objects.create(
        category_id=thread.category_id,
        thread_id=thread.id,
        starter_id=None,
        title=thread.title,
        started_at=thread.started_at,
    )

    post_search = PostSearch.objects.create(
        category_id=post.category_id,
        thread_id=post.thread_id,
        post_id=post.id,
        poster_id=None,
        content=post.content,
        posted_at=post.posted_at,
    )

    stdout, stderr = call_command()

    assert stdout == (
        'Cleared the search index using the "PostgreSQL full-text search" backend.',
        "",
        "Time: 0.00s",
    )
    assert not stderr

    with pytest.raises(ThreadSearch.DoesNotExist):
        thread_search.refresh_from_db()

    with pytest.raises(PostSearch.DoesNotExist):
        post_search.refresh_from_db()


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
