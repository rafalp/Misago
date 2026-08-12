import pytest

from ...threads.enums import ThreadPinned
from ...threads.synchronize import synchronize_thread
from ..backends import PostgreSQLSearchBackend
from ..models import PostSearch, ThreadSearch


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

    backend.index_threads([thread, other_thread])
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


def test_postgresql_backend_index_threads_indexes_threads(
    thread_factory, backend, default_category, other_category, user, other_user
):
    thread = thread_factory(
        default_category,
        starter=user,
        title="Plugin hook for post validation",
    )
    deleted_user_thread = thread_factory(
        other_category,
        starter="DeletedUser",
        title="Forum software recommendations",
    )
    pinned_thread = thread_factory(
        default_category,
        starter=other_user,
        title="Important announcement: please read",
        pinned=ThreadPinned.EVERYWHERE,
    )

    backend.index_threads([thread, deleted_user_thread, pinned_thread])

    thread_search = ThreadSearch.objects.get(thread_id=thread.id)
    assert thread_search.category_id == default_category.id
    assert thread_search.starter_id == user.id
    assert thread_search.title == thread.title
    assert thread_search.started_at == thread.started_at
    assert not thread_search.is_pinned

    deleted_user_thread_search = ThreadSearch.objects.get(
        thread_id=deleted_user_thread.id
    )
    assert deleted_user_thread_search.category_id == other_category.id
    assert deleted_user_thread_search.starter_id is None
    assert deleted_user_thread_search.title == deleted_user_thread.title
    assert deleted_user_thread_search.started_at == deleted_user_thread.started_at
    assert not deleted_user_thread_search.is_pinned

    pinned_thread_search = ThreadSearch.objects.get(thread_id=pinned_thread.id)
    assert pinned_thread_search.category_id == pinned_thread.id
    assert pinned_thread_search.starter_id == other_user.id
    assert pinned_thread_search.title == pinned_thread.title
    assert pinned_thread_search.started_at == pinned_thread.started_at
    assert pinned_thread_search.is_pinned


def test_postgresql_backend_index_threads_escapes_thread_titles(
    thread_factory, backend, default_category
):
    thread = thread_factory(
        default_category,
        starter="Moderator",
        title="<mark></mark> in search results",
    )

    backend.index_threads([thread])

    thread_search = ThreadSearch.objects.get(thread_id=thread.id)
    assert thread_search.category_id == default_category.id
    assert thread_search.starter_id is None
    assert thread_search.title == "&lt;mark&gt;&lt;/mark&gt; in search results"
    assert thread_search.started_at == thread.started_at
    assert not thread_search.is_pinned


def test_postgresql_backend_index_posts_indexes_posts(
    thread_factory, thread_reply_factory, backend, default_category, user, other_user
):
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

    first_post_search = PostSearch.objects.get(post_id=first_post.id)
    assert first_post_search.category_id == first_post.category_id
    assert first_post_search.thread_id == first_post.thread_id
    assert first_post_search.poster_id == first_post.poster_id
    assert first_post_search.content
    assert first_post_search.posted_at == first_post.posted_at
    assert not first_post_search.is_thread_pinned
    assert not first_post_search.incoming_links
    assert not first_post_search.is_hidden
    assert not first_post_search.is_unapproved

    hidden_reply_search = PostSearch.objects.get(post_id=hidden_reply.id)
    assert hidden_reply_search.category_id == hidden_reply.category_id
    assert hidden_reply_search.thread_id == hidden_reply.thread_id
    assert not hidden_reply_search.poster_id
    assert hidden_reply_search.content
    assert hidden_reply_search.posted_at == hidden_reply.posted_at
    assert not hidden_reply_search.is_thread_pinned
    assert not hidden_reply_search.incoming_links
    assert hidden_reply_search.is_hidden
    assert not hidden_reply_search.is_unapproved

    reply_search = PostSearch.objects.get(post_id=reply.id)
    assert reply_search.category_id == reply_search.category_id
    assert reply_search.thread_id == reply_search.thread_id
    assert reply_search.poster_id == reply_search.poster_id
    assert reply_search.content
    assert reply_search.posted_at == reply_search.posted_at
    assert not reply_search.is_thread_pinned
    assert not reply_search.incoming_links
    assert not reply_search.is_hidden
    assert not reply_search.is_unapproved


def test_postgresql_backend_index_posts_reindexes_existing_posts(
    thread_reply_factory, backend, user, thread
):
    post = thread_reply_factory(thread, poster=user, content="Hello world")
    backend.index_posts([(post, post.content)])

    post_search = PostSearch.objects.get(post_id=post.id)
    assert not post_search.is_hidden

    post.is_hidden = True
    post.save()

    backend.index_posts([(post, post.content)])

    post_search.refresh_from_db()
    assert post_search.is_hidden


def test_postgresql_backend_index_posts_escapes_posts_html(
    thread_factory, backend, default_category
):
    thread = thread_factory(default_category, title="Test <b>thread</b>")

    post = thread.first_post
    post.content = "Hello <b>world</b>"
    post.save()

    backend.index_posts([(post, post.content)])

    post_search = PostSearch.objects.get(post_id=post.id)
    assert post_search.content == "Hello &lt;b&gt;world&lt;/b&gt;"


def test_postgresql_backend_searches_thread_titles(
    user_permissions_factory, backend, search_index, user, default_category
):
    user_permissions = user_permissions_factory(user)

    results = backend.search_thread_titles(
        "forum software",
        user_permissions,
        categories=[default_category],
    )

    assert results.count == 1

    result = results.results[0]
    assert result.post_id == search_index["first_post"].id
    assert result.thread_title == "<hl>Forum</hl> <hl>software</hl> recommendations?"
    assert result.post_content == (
        "I am looking for a good <hl>forum</hl> <hl>software</hl> for my next project."
        " "
        "Any recommendations?"
    )


def test_postgresql_backend_thread_titles_search_handles_empty_result(
    user_permissions_factory, backend, user, default_category
):
    user_permissions = user_permissions_factory(user)

    results = backend.search_thread_titles(
        "lorem ipsum",
        user_permissions,
        categories=[default_category],
    )

    assert results.count == 0


def test_postgresql_backend_search_searches_threads(
    user_permissions_factory, backend, search_index, user, default_category
):
    user_permissions = user_permissions_factory(user)

    results = backend.search_threads(
        "forum software",
        user_permissions,
        categories=[default_category],
    )

    results_ids = [result.post_id for result in results]
    assert search_index["first_post"].id in results_ids


def test_postgresql_backend_thread_search_handles_empty_result(
    user_permissions_factory, backend, search_index, user, default_category
):
    user_permissions = user_permissions_factory(user)

    results = backend.search_threads(
        "lorem ipsum",
        user_permissions,
        categories=[default_category],
    )

    assert results.count == 0


def test_postgresql_backend_search_searches_posts(
    user_permissions_factory, backend, search_index, user, default_category
):
    user_permissions = user_permissions_factory(user)

    results = backend.search_posts(
        "forum software",
        user_permissions,
        categories=[default_category],
    )

    results_ids = [result.post_id for result in results]
    assert search_index["first_post"].id in results_ids


def test_postgresql_backend_post_search_handles_empty_result(
    user_permissions_factory, backend, search_index, user, default_category
):
    user_permissions = user_permissions_factory(user)

    results = backend.search_posts(
        "lorem ipsum",
        user_permissions,
        categories=[default_category],
    )

    assert results.count == 0


def test_postgresql_backend_update_category_updates_threads_and_posts_categories_by_category(
    thread_factory,
    thread_reply_factory,
    backend,
    default_category,
    sibling_category,
    other_category,
):
    thread = thread_factory(default_category)
    other_thread = thread_factory(sibling_category)

    post = thread_reply_factory(thread)
    other_post = thread_reply_factory(other_thread)

    backend.index_threads([thread, other_thread])
    backend.index_posts([(post, post.content), (other_post, other_post.content)])

    updated = backend.update_category(other_category, categories=[default_category])
    assert updated == 2

    thread_search = ThreadSearch.objects.get(thread_id=thread.id)
    assert thread_search.category_id == other_category.id

    other_thread_search = ThreadSearch.objects.get(thread_id=other_thread.id)
    assert other_thread_search.category_id == sibling_category.id

    post_search = PostSearch.objects.get(post_id=post.id)
    assert post_search.category_id == other_category.id

    other_post_search = PostSearch.objects.get(post_id=other_post.id)
    assert other_post_search.category_id == sibling_category.id


def test_postgresql_backend_update_category_updates_threads_and_posts_categories_by_thread(
    thread_factory,
    thread_reply_factory,
    backend,
    default_category,
    sibling_category,
    other_category,
):
    thread = thread_factory(default_category)
    other_thread = thread_factory(sibling_category)

    post = thread_reply_factory(thread)
    other_post = thread_reply_factory(other_thread)

    backend.index_threads([thread, other_thread])
    backend.index_posts([(post, post.content), (other_post, other_post.content)])

    updated = backend.update_category(other_category, threads=[thread])
    assert updated == 2

    thread_search = ThreadSearch.objects.get(thread_id=thread.id)
    assert thread_search.category_id == other_category.id

    other_thread_search = ThreadSearch.objects.get(thread_id=other_thread.id)
    assert other_thread_search.category_id == sibling_category.id

    post_search = PostSearch.objects.get(post_id=post.id)
    assert post_search.category_id == other_category.id

    other_post_search = PostSearch.objects.get(post_id=other_post.id)
    assert other_post_search.category_id == sibling_category.id


def test_postgresql_backend_update_thread_updates_posts_by_thread(
    thread_factory,
    thread_reply_factory,
    backend,
    default_category,
    sibling_category,
    other_category,
):
    thread = thread_factory(default_category)
    new_thread = thread_factory(other_category)
    other_thread = thread_factory(sibling_category)

    post = thread_reply_factory(thread)
    other_post = thread_reply_factory(other_thread)

    backend.index_threads([thread, new_thread, other_thread])
    backend.index_posts([(post, post.content), (other_post, other_post.content)])

    updated = backend.update_thread(new_thread, threads=[thread])
    assert updated == 1

    post_search = PostSearch.objects.get(post_id=post.id)
    assert post_search.category_id == other_category.id
    assert post_search.thread_id == new_thread.id

    other_post_search = PostSearch.objects.get(post_id=other_post.id)
    assert other_post_search.category_id == sibling_category.id
    assert other_post_search.thread_id == other_thread.id


def test_postgresql_backend_update_thread_updates_posts_by_post(
    thread_factory,
    thread_reply_factory,
    backend,
    default_category,
    sibling_category,
    other_category,
):
    thread = thread_factory(default_category)
    new_thread = thread_factory(other_category)
    other_thread = thread_factory(sibling_category)

    post = thread_reply_factory(thread)
    other_post = thread_reply_factory(other_thread)

    backend.index_threads([thread, new_thread, other_thread])
    backend.index_posts([(post, post.content), (other_post, other_post.content)])

    updated = backend.update_thread(new_thread, posts=[post])
    assert updated == 1

    post_search = PostSearch.objects.get(post_id=post.id)
    assert post_search.category_id == other_category.id
    assert post_search.thread_id == new_thread.id

    other_post_search = PostSearch.objects.get(post_id=other_post.id)
    assert other_post_search.category_id == sibling_category.id
    assert other_post_search.thread_id == other_thread.id


def test_postgresql_backend_delete_categories_deletes_threads_and_posts_in_category(
    thread_factory, thread_reply_factory, backend, default_category, other_category
):
    thread = thread_factory(default_category)
    other_thread = thread_factory(other_category)

    post = thread_reply_factory(thread)
    other_post = thread_reply_factory(other_thread)

    backend.index_threads([thread, other_thread])
    backend.index_posts([(post, post.content), (other_post, other_post.content)])

    deleted = backend.delete_categories([default_category])
    assert deleted == 2

    with pytest.raises(ThreadSearch.DoesNotExist):
        ThreadSearch.objects.get(thread_id=thread.id)

    ThreadSearch.objects.get(thread_id=other_thread.id)

    with pytest.raises(PostSearch.DoesNotExist):
        PostSearch.objects.get(post_id=post.id)

    PostSearch.objects.get(post_id=other_post.id)


def test_postgresql_backend_delete_threads_deletes_thread_and_its_posts(
    thread_factory, thread_reply_factory, backend, default_category
):
    thread = thread_factory(default_category)
    other_thread = thread_factory(default_category)

    post = thread_reply_factory(thread)
    other_post = thread_reply_factory(other_thread)

    backend.index_threads([thread, other_thread])
    backend.index_posts([(post, post.content), (other_post, other_post.content)])

    deleted = backend.delete_threads([thread])
    assert deleted == 2

    with pytest.raises(ThreadSearch.DoesNotExist):
        ThreadSearch.objects.get(thread_id=thread.id)

    ThreadSearch.objects.get(thread_id=other_thread.id)

    with pytest.raises(PostSearch.DoesNotExist):
        PostSearch.objects.get(post_id=post.id)

    PostSearch.objects.get(post_id=other_post.id)


def test_postgresql_backend_delete_posts_deletes_posts(
    thread_factory, thread_reply_factory, backend, default_category
):
    thread = thread_factory(default_category)
    other_thread = thread_factory(default_category)

    post = thread_reply_factory(thread)
    other_post = thread_reply_factory(other_thread)

    backend.index_threads([thread, other_thread])
    backend.index_posts([(post, post.content), (other_post, other_post.content)])

    deleted = backend.delete_posts([post])
    assert deleted == 1

    ThreadSearch.objects.get(thread_id=thread.id)
    ThreadSearch.objects.get(thread_id=other_thread.id)

    with pytest.raises(PostSearch.DoesNotExist):
        PostSearch.objects.get(post_id=post.id)

    PostSearch.objects.get(post_id=other_post.id)


def test_postgresql_backend_clear_deletes_all_posts(
    thread_factory, thread_reply_factory, backend, default_category
):
    thread = thread_factory(default_category)
    other_thread = thread_factory(default_category)

    post = thread_reply_factory(thread)
    other_post = thread_reply_factory(other_thread)

    backend.index_threads([thread, other_thread])
    backend.index_posts([(post, post.content), (other_post, other_post.content)])

    backend.clear()

    assert not ThreadSearch.objects.exists()
    assert not PostSearch.objects.exists()
