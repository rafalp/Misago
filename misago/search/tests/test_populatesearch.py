from io import StringIO

from django.core import management

from ...privatethreads.members import get_private_thread_members
from ..exceptions import SearchBackendError
from ..management.commands import populatesearch
from ..models import PostSearch, ThreadSearch


def call_command(**kwargs):
    command = populatesearch.Command()

    stdout = StringIO()
    stderr = StringIO()

    management.call_command(command, stdout=stdout, stderr=stderr, **kwargs)
    return (
        tuple(l.strip() for l in stdout.getvalue().strip().splitlines()),
        tuple(l.strip() for l in stderr.getvalue().strip().splitlines()),
    )


def test_populatesearch_indexes_threads_and_posts(thread, post):
    stdout, stderr = call_command()

    ThreadSearch.objects.get(thread_id=thread.id)
    PostSearch.objects.get(post_id=post.id)

    assert stdout[0] == 'Populating "PostgreSQL full-text search"...'
    assert stdout[2].startswith("Cleared existing search data in ")
    assert stdout[-1].startswith("Indexed one post in ")

    assert not stderr


def test_populatesearch_command_clears_search_index(thread, post):
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

    assert stdout[0] == 'Populating "PostgreSQL full-text search"...'
    assert stdout[2].startswith("Cleared existing search data in ")
    assert stdout[-1].startswith("Indexed one post in ")

    assert not stderr

    thread_search.refresh_from_db()
    post_search.refresh_from_db()


def test_populatesearch_command_indexes_private_thread_members(
    mocker, thread, post, user_private_thread
):
    mock_update_thread_members = mocker.patch(
        "misago.search.service.search.update_thread_members", autospec=True
    )

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

    assert stdout[0] == 'Populating "PostgreSQL full-text search"...'
    assert stdout[2].startswith("Cleared existing search data in ")
    assert stdout[-1].startswith("Indexed 2 posts in ")

    assert not stderr

    thread_search.refresh_from_db()
    post_search.refresh_from_db()

    _, private_thread_members = get_private_thread_members(user_private_thread)
    mock_update_thread_members.assert_called_once_with(
        user_private_thread, [user.id for user in private_thread_members]
    )


def test_populatesearch_command_skips_search_index_clear_on_option(thread, post):
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

    stdout, stderr = call_command(no_clear=True)

    assert stdout[0] == 'Populating "PostgreSQL full-text search"...'
    assert stdout[2] == "Keeping existing search data."
    assert stdout[-1].startswith("Indexed one post in ")

    assert not stderr

    thread_search.refresh_from_db()
    post_search.refresh_from_db()


def test_populatesearch_command_prints_clear_error(mocker, db):
    mocker.patch(
        "misago.search.service.search.backend.clear",
        side_effect=SearchBackendError("This backend is not available."),
    )

    stdout, stderr = call_command()

    assert stdout == ('Populating "PostgreSQL full-text search"...',)
    assert stderr == (
        "Error clearing search data:",
        "",
        "This backend is not available.",
    )
