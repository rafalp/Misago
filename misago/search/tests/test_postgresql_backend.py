import pytest

from ...threads.synchronize import synchronize_thread
from ..backends import PostgreSQLSearchBackend
from ..models import PostSearch


@pytest.fixture
def backend(db):
    return PostgreSQLSearchBackend({"PG_SEARCH_CONFIG": "english"})


def test_postgresql_backend_initialize_does_nothing(backend):
    backend.initialize()


def test_postgresql_backend_index_posts_indexes_posts(
    thread_factory, thread_reply_factory, backend, default_category, user, other_user
):
    backend.initialize()

    thread = thread_factory(
        default_category,
        starter=user,
        title="Plugin hook for post validation",
    )

    first_post = thread.first_post
    first_post.thread = thread
    first_post.content = (
        "I am looking for a plugin hook to use for custom post validator."
    )
    first_post.save()

    hidden_reply = thread_reply_factory(
        thread,
        poster="HiddenUser",
        content="Test test test",
        is_hidden=True,
    )
    reply = thread_reply_factory(
        thread,
        poster=other_user,
        content="Please see the validate_post_content_hook from misago.posting",
    )

    synchronize_thread(first_post.thread)

    backend.index_posts(
        [(post, post.content) for post in [first_post, hidden_reply, reply]]
    )

    first_post_document = PostSearch.objects.get(post_id=first_post.id)
    assert first_post_document.category_id == first_post.category_id
    assert first_post_document.thread_id == first_post.thread_id
    assert first_post_document.poster_id == first_post.poster_id
    assert first_post_document.thread_title
    assert first_post_document.post_content
    assert first_post_document.posted_at == first_post.posted_at
    assert not first_post_document.is_thread_pinned
    assert not first_post_document.incoming_links
    assert not first_post_document.is_hidden
    assert not first_post_document.is_unapproved

    hidden_reply_document = PostSearch.objects.get(post_id=hidden_reply.id)
    assert hidden_reply_document.category_id == hidden_reply.category_id
    assert hidden_reply_document.thread_id == hidden_reply.thread_id
    assert not hidden_reply_document.poster_id
    assert not hidden_reply_document.thread_title
    assert hidden_reply_document.post_content
    assert hidden_reply_document.posted_at == hidden_reply.posted_at
    assert not hidden_reply_document.is_thread_pinned
    assert not hidden_reply_document.incoming_links
    assert hidden_reply_document.is_hidden
    assert not hidden_reply_document.is_unapproved

    reply_document = PostSearch.objects.get(post_id=reply.id)
    assert reply_document.category_id == reply_document.category_id
    assert reply_document.thread_id == reply_document.thread_id
    assert reply_document.poster_id == reply_document.poster_id
    assert not reply_document.thread_title
    assert reply_document.post_content
    assert reply_document.posted_at == reply_document.posted_at
    assert not reply_document.is_thread_pinned
    assert not reply_document.incoming_links
    assert not reply_document.is_hidden
    assert not reply_document.is_unapproved


def test_postgresql_backend_index_posts_reindexes_existing_posts(
    thread_reply_factory, backend, user, thread
):
    post = thread_reply_factory(thread, poster=user, content="Hello world")
    backend.index_posts([(post, post.content)])

    post_document = PostSearch.objects.get(post_id=post.id)
    assert not post_document.is_hidden

    post.is_hidden = True
    post.save()

    backend.index_posts([(post, post.content)])

    post_document.refresh_from_db()
    assert post_document.is_hidden
