from io import StringIO

import pytest
from django.core import management

from ..exceptions import SearchBackendError
from ..management.commands import buildsearchindex
from ..models import PostSearch, ThreadSearch


def call_command(**kwargs):
    command = buildsearchindex.Command()

    stdout = StringIO()
    stderr = StringIO()

    management.call_command(command, stdout=stdout, stderr=stderr, **kwargs)
    return (
        tuple(l.strip() for l in stdout.getvalue().strip().splitlines()),
        tuple(l.strip() for l in stderr.getvalue().strip().splitlines()),
    )


def test_buildsearchindex_indexes_threads_and_posts(thread, post):
    stdout, stderr = call_command()

    ThreadSearch.objects.get(thread_id=thread.id)
    PostSearch.objects.get(post_id=post.id)

    assert stdout[0] == (
        'Rebuilding the search index using the "PostgreSQL full-text search" backend.'
    )
    assert stdout[2].startswith("Cleared the search index in ")
    assert stdout[-1].startswith("Indexed one post in ")

    assert not stderr


def test_buildsearchindex_command_clears_search_index(thread, post):
    thread_search = ThreadSearch.objects.create(
        category_id=thread.category_id * 10,
        thread_id=thread.id * 10,
        starter_id=None,
        title="Doesnt exist",
        started_at=thread.started_at,
    )

    post_search = PostSearch.objects.create(
        category_id=post.category_id * 10,
        thread_id=post.thread_id * 10,
        post_id=post.id * 10,
        poster_id=None,
        content=post.content,
        posted_at=post.posted_at,
    )

    stdout, stderr = call_command()

    assert stdout[0] == (
        'Rebuilding the search index using the "PostgreSQL full-text search" backend.'
    )
    assert stdout[2].startswith("Cleared the search index in ")
    assert stdout[-1].startswith("Indexed one post in ")

    assert not stderr

    with pytest.raises(ThreadSearch.DoesNotExist):
        thread_search.refresh_from_db()

    with pytest.raises(PostSearch.DoesNotExist):
        post_search.refresh_from_db()


def test_buildsearchindex_command_skips_search_index_clear_on_option(thread, post):
    thread_search = ThreadSearch.objects.create(
        category_id=thread.category_id * 10,
        thread_id=thread.id * 10,
        starter_id=None,
        title="Doesnt exist",
        started_at=thread.started_at,
    )

    post_search = PostSearch.objects.create(
        category_id=post.category_id * 10,
        thread_id=post.thread_id * 10,
        post_id=post.id * 10,
        poster_id=None,
        content=post.content,
        posted_at=post.posted_at,
    )

    stdout, stderr = call_command(skip_clear=True)

    assert stdout[0] == (
        'Rebuilding the search index using the "PostgreSQL full-text search" backend.'
    )
    assert stdout[2].startswith("Skipped clearing the search index.")
    assert stdout[-1].startswith("Indexed one post in ")

    assert not stderr

    thread_search.refresh_from_db()
    post_search.refresh_from_db()


def test_buildsearchindex_command_prints_clear_error(mocker, db):
    mocker.patch(
        "misago.search.posts.posts_search.backend.clear",
        side_effect=SearchBackendError("This backend is not available."),
    )

    stdout, stderr = call_command()

    assert stdout == (
        'Rebuilding the search index using the "PostgreSQL full-text search" backend.',
    )
    assert stderr == (
        "Error clearing the search index:",
        "",
        "This backend is not available.",
    )
