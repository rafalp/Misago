import pytest

from ...threads.models import Thread
from ...threads.synchronize import synchronize_thread
from ..backends import PostgreSQLSearchBackend
from ..enums import SearchMode
from ..models import PostSearch


@pytest.fixture
def backend(db):
    return PostgreSQLSearchBackend({"PG_SEARCH_CONFIG": "english"})


@pytest.fixture
def search_index(
    thread_factory,
    thread_reply_factory,
    backend,
    user,
    other_user,
    default_category,
    other_category,
):
    thread = thread_factory(
        default_category,
        starter=user,
        title="Forum software recommendations?",
    )

    first_post = thread.first_post
    first_post.thread = thread
    first_post.content = "I am looking for a good forum software for my next project. Any recommendations?"
    first_post.save()

    hidden_reply = thread_reply_factory(
        thread,
        poster="HiddenUser",
        content="phpBB by Przemo",
        is_hidden=True,
    )
    unapproved_reply = thread_reply_factory(
        thread,
        poster=other_user,
        content="Try FluxBB",
        is_hidden=False,
    )
    reply = thread_reply_factory(
        thread,
        poster=other_user,
        content="Give Misago a chance. This site runs it and we are happy with it.",
    )

    other_thread = thread_factory(
        default_category,
        starter=user,
        title="Plugin hook for post validation",
    )
    other_thread_first_post = other_thread.first_post
    other_thread_first_post.thread = other_thread
    other_thread_first_post.content = (
        "I am looking for a plugin hook to use for custom post validator."
    )
    other_thread_first_post.save()

    other_thread_reply = thread_reply_factory(
        thread,
        poster=other_user,
        content="Please see the validate_post_content_hook from misago.posting",
    )

    posts = [
        first_post,
        hidden_reply,
        unapproved_reply,
        reply,
        other_thread_first_post,
        other_thread_reply,
    ]

    synchronize_thread(first_post.thread)
    synchronize_thread(other_thread_reply.thread)

    backend.index_posts([(post, post.content) for post in posts])

    return {
        "thread": thread,
        "first_post": first_post,
        "hidden_reply": hidden_reply,
        "unapproved_reply": unapproved_reply,
        "reply": reply,
        "other_thread": other_thread,
        "other_thread_reply": other_thread_reply,
    }


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


def test_postgresql_backend_search_searches_posts(
    user_permissions_factory, backend, search_index, user, default_category
):
    user_permissions = user_permissions_factory(user)

    results = backend.search_posts(
        "forum software",
        SearchMode.THREADS,
        user_permissions,
        categories=[default_category],
    )

    results_ids = [result.post_id for result in results]
    assert search_index["first_post"].id in results_ids


def test_postgresql_backend_move_category_posts_moves_category_posts_to_new_category(
    thread_reply_factory, backend, default_category, other_category, thread
):
    post = thread_reply_factory(thread, poster="User", content="Hello world")
    backend.index_posts([(post, post.content)])

    post_document = PostSearch.objects.get(post_id=post.id)
    assert post_document.category_id == default_category.id

    backend.move_category_posts([default_category], other_category)

    post_document.refresh_from_db()
    assert post_document.category_id == other_category.id


def test_postgresql_backend_move_thread_posts_moves_thread_posts_to_new_thread(
    thread_factory, thread_reply_factory, backend, default_category, other_category
):
    thread = thread_factory(default_category)
    post = thread_reply_factory(thread, poster="User", content="Hello world")
    backend.index_posts([(post, post.content)])

    post_document = PostSearch.objects.get(post_id=post.id)
    assert post_document.thread_id == thread.id

    other_thread = thread_factory(other_category)
    backend.move_thread_posts([thread], other_thread)

    post_document.refresh_from_db()
    assert post_document.category_id == other_category.id
    assert post_document.thread_id == other_thread.id


def test_postgresql_backend_move_threads_moves_threads_to_new_category(
    thread_reply_factory, backend, default_category, other_category, thread
):
    post = thread_reply_factory(thread, poster="User", content="Hello world")
    backend.index_posts([(post, post.content)])

    post_document = PostSearch.objects.get(post_id=post.id)
    assert post_document.category_id == default_category.id

    backend.move_threads([thread], other_category)

    post_document.refresh_from_db()
    assert post_document.category_id == other_category.id


def test_postgresql_backend_move_posts_moves_posts_to_new_thread(
    thread_factory, thread_reply_factory, backend, default_category, other_category
):
    thread = thread_factory(default_category)
    post = thread_reply_factory(thread, poster="User", content="Hello world")
    backend.index_posts([(post, post.content)])

    other_thread = thread_factory(other_category)

    post_document = PostSearch.objects.get(post_id=post.id)
    assert post_document.thread_id == thread.id

    backend.move_posts([post], other_thread)

    post_document.refresh_from_db()
    assert post_document.category_id == other_category.id
    assert post_document.thread_id == other_thread.id


def test_postgresql_backend_delete_categories_deletes_posts_in_category(
    thread_factory, thread_reply_factory, backend, default_category, other_category
):
    thread = thread_factory(default_category)
    post = thread_reply_factory(thread, poster="User", content="Hello world")
    backend.index_posts([(post, post.content)])

    other_thread = thread_factory(other_category)
    other_post = thread_reply_factory(
        other_thread, poster="User", content="Lorem ipsum"
    )
    backend.index_posts([(other_post, other_post.content)])

    backend.delete_categories([default_category])

    with pytest.raises(PostSearch.DoesNotExist):
        PostSearch.objects.get(post_id=post.id)

    PostSearch.objects.get(post_id=other_post.id)


def test_postgresql_backend_delete_threads_deletes_posts_in_thread(
    thread_factory, thread_reply_factory, backend, default_category
):
    thread = thread_factory(default_category)
    post = thread_reply_factory(thread, poster="User", content="Hello world")
    backend.index_posts([(post, post.content)])

    other_thread = thread_factory(default_category)
    other_post = thread_reply_factory(
        other_thread, poster="User", content="Lorem ipsum"
    )
    backend.index_posts([(other_post, other_post.content)])

    backend.delete_threads([thread])

    with pytest.raises(PostSearch.DoesNotExist):
        PostSearch.objects.get(post_id=post.id)

    PostSearch.objects.get(post_id=other_post.id)


def test_postgresql_backend_delete_posts_deletes_posts(
    thread_factory, thread_reply_factory, backend, default_category
):
    thread = thread_factory(default_category)
    post = thread_reply_factory(thread, poster="User", content="Hello world")
    backend.index_posts([(post, post.content)])

    other_thread = thread_factory(default_category)
    other_post = thread_reply_factory(
        other_thread, poster="User", content="Lorem ipsum"
    )
    backend.index_posts([(other_post, other_post.content)])

    backend.delete_posts([post])

    with pytest.raises(PostSearch.DoesNotExist):
        PostSearch.objects.get(post_id=post.id)

    PostSearch.objects.get(post_id=other_post.id)


def test_postgresql_backend_delete_users_deletes_posts_by_user(
    thread_factory, thread_reply_factory, backend, user, other_user, default_category
):
    thread = thread_factory(default_category)
    post = thread_reply_factory(thread, poster=user, content="Hello world")
    backend.index_posts([(post, post.content)])

    other_thread = thread_factory(default_category)
    other_post = thread_reply_factory(
        other_thread, poster=other_user, content="Lorem ipsum"
    )
    backend.index_posts([(other_post, other_post.content)])

    backend.delete_users([user])

    with pytest.raises(PostSearch.DoesNotExist):
        PostSearch.objects.get(post_id=post.id)

    PostSearch.objects.get(post_id=other_post.id)


def test_postgresql_backend_clear_deletes_all_posts(
    thread_factory, thread_reply_factory, backend, user, other_user, default_category
):
    thread = thread_factory(default_category)
    post = thread_reply_factory(thread, poster=user, content="Hello world")
    backend.index_posts([(post, post.content)])

    other_thread = thread_factory(default_category)
    other_post = thread_reply_factory(
        other_thread, poster=other_user, content="Lorem ipsum"
    )
    backend.index_posts([(other_post, other_post.content)])

    backend.clear()

    assert not PostSearch.objects.exists()
