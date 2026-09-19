import pytest
from django.contrib.postgres.search import SearchQuery

from ...threads.enums import ThreadPinned
from ...threads.synchronize import synchronize_thread
from ..backends import PostgreSQLSearchBackend
from ..enums import SearchMode
from ..models import PostSearch, ThreadSearch


@pytest.fixture
def backend(db):
    return PostgreSQLSearchBackend({"PG_SEARCH_CONFIG": "english"})


def test_postgresql_backend_initialize_does_nothing(backend):
    backend.initialize()


def test_postgresql_backend_search_threads_searches_threads(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    backend,
    default_category,
):
    databases_thread = thread_factory(
        default_category, title="Database engine recommendation"
    )
    mysql_post = thread_reply_factory(databases_thread)
    postgresql_post = thread_reply_factory(databases_thread)

    cars_thread = thread_factory(default_category, title="Favorite car?")
    seat_post = thread_reply_factory(cars_thread)
    nissan_post = thread_reply_factory(cars_thread)

    synchronize_thread(databases_thread)
    synchronize_thread(cars_thread)

    backend.index_threads([databases_thread, cars_thread])
    backend.index_posts(
        [
            (mysql_post, "MySQL is OpenSource and widely available."),
            (postgresql_post, "PostgreSQL has great features!"),
            (seat_post, "I love SEAT"),
            (nissan_post, "I drive Nissan"),
        ]
    )

    user_permissions = user_permissions_factory(user)

    results = backend.search_threads(
        "postgresql database", user_permissions, categories=[default_category]
    )

    assert len(results.items) == 1
    assert results.items[0].post_id == postgresql_post.id


def test_postgresql_backend_search_threads_searches_thread_titles(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    backend,
    default_category,
):
    databases_thread = thread_factory(
        default_category, title="Database engine recommendation"
    )
    databases_post = databases_thread.first_post
    mysql_post = thread_reply_factory(databases_thread)
    postgresql_post = thread_reply_factory(databases_thread)

    cars_thread = thread_factory(default_category, title="Favorite car?")
    cars_post = cars_thread.first_post
    seat_post = thread_reply_factory(cars_thread)
    nissan_post = thread_reply_factory(cars_thread)

    synchronize_thread(databases_thread)
    synchronize_thread(cars_thread)

    backend.index_threads([databases_thread, cars_thread])
    backend.index_posts(
        [
            (databases_post, "What are you using?"),
            (mysql_post, "MySQL is OpenSource and widely available."),
            (postgresql_post, "PostgreSQL has great features!"),
            (cars_post, "What are you driving?"),
            (seat_post, "I love SEAT"),
            (nissan_post, "I drive Nissan"),
        ]
    )

    user_permissions = user_permissions_factory(user)

    results = backend.search_threads(
        "database",
        user_permissions,
        categories=[default_category],
        mode=SearchMode.THREAD_TITLES,
    )

    assert len(results.items) == 1
    assert results.items[0].post_id == databases_post.id


def test_postgresql_backend_search_threads_searches_thread_posts(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    backend,
    default_category,
):
    databases_thread = thread_factory(
        default_category, title="Database engine recommendation"
    )
    mysql_post = thread_reply_factory(databases_thread)
    postgresql_post = thread_reply_factory(databases_thread)

    cars_thread = thread_factory(default_category, title="Favorite car?")
    seat_post = thread_reply_factory(cars_thread)
    nissan_post = thread_reply_factory(cars_thread)

    synchronize_thread(databases_thread)
    synchronize_thread(cars_thread)

    backend.index_threads([databases_thread, cars_thread])
    backend.index_posts(
        [
            (mysql_post, "MySQL is OpenSource and widely available."),
            (postgresql_post, "PostgreSQL has great features!"),
            (seat_post, "I love SEAT"),
            (nissan_post, "I drive Nissan"),
        ]
    )

    user_permissions = user_permissions_factory(user)

    results = backend.search_threads(
        "seat",
        user_permissions,
        categories=[default_category],
        mode=SearchMode.POSTS,
    )

    assert len(results.items) == 1
    assert results.items[0].post_id == seat_post.id


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

    thread_search = ThreadSearch.objects.get(thread=thread)
    assert thread_search.category_id == default_category.id
    assert thread_search.starter_id == user.id
    assert thread_search.title == thread.title
    assert thread_search.started_at == thread.started_at

    deleted_user_thread_search = ThreadSearch.objects.get(thread=deleted_user_thread)
    assert deleted_user_thread_search.category_id == other_category.id
    assert deleted_user_thread_search.starter_id is None
    assert deleted_user_thread_search.title == deleted_user_thread.title
    assert deleted_user_thread_search.started_at == deleted_user_thread.started_at


def test_postgresql_backend_index_threads_escapes_thread_titles(
    thread_factory, backend, default_category
):
    thread = thread_factory(
        default_category,
        starter="Moderator",
        title="<mark></mark> in search results",
    )

    backend.index_threads([thread])

    thread_search = ThreadSearch.objects.get(thread=thread)
    assert thread_search.category_id == default_category.id
    assert thread_search.starter_id is None
    assert thread_search.title == "&lt;mark&gt;&lt;/mark&gt; in search results"
    assert thread_search.started_at == thread.started_at


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

    reply = thread_reply_factory(
        thread,
        poster=other_user,
        content="Please see the validate_post_content_hook from misago.posting",
    )

    synchronize_thread(first_post.thread)

    backend.index_posts([(post, post.content) for post in [first_post, reply]])

    first_post_search = PostSearch.objects.get(post=first_post)
    assert first_post_search.category_id == first_post.category_id
    assert first_post_search.thread_id == first_post.thread_id
    assert first_post_search.poster_id == first_post.poster_id
    assert first_post_search.content
    assert first_post_search.posted_at == first_post.posted_at

    reply_search = PostSearch.objects.get(post=reply)
    assert reply_search.category_id == reply_search.category_id
    assert reply_search.thread_id == reply_search.thread_id
    assert reply_search.poster_id == reply_search.poster_id
    assert reply_search.content
    assert reply_search.posted_at == reply_search.posted_at


def test_postgresql_backend_index_posts_reindexes_existing_posts(
    thread_reply_factory, backend, user, thread
):
    post = thread_reply_factory(thread, poster=user, content="Hello world")
    backend.index_posts([(post, post.content)])

    post_search = PostSearch.objects.get(post=post)
    assert post_search.content == "Hello world"

    post.content = "Updated"
    post.save()

    backend.index_posts([(post, post.content)])

    post_search.refresh_from_db()
    assert post_search.content == "Updated"


def test_postgresql_backend_index_posts_escapes_posts_html(
    thread_factory, backend, default_category
):
    thread = thread_factory(default_category, title="Test <b>thread</b>")

    post = thread.first_post
    post.content = "Hello <b>world</b>"
    post.save()

    backend.index_posts([(post, post.content)])

    post_search = PostSearch.objects.get(post=post)
    assert post_search.content == "Hello &lt;b&gt;world&lt;/b&gt;"


def _test_postgresql_backend_searches_thread_titles(
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
    assert result.post_id == ["first_post"].id
    assert result.thread_title == "<hl>Forum</hl> <hl>software</hl> recommendations?"
    assert result.post_content == (
        "I am looking for a good <hl>forum</hl> <hl>software</hl> for my next project."
        " "
        "Any recommendations?"
    )


def _test_postgresql_backend_thread_titles_search_handles_empty_result(
    user_permissions_factory, backend, user, default_category
):
    user_permissions = user_permissions_factory(user)

    results = backend.search_thread_titles(
        "lorem ipsum",
        user_permissions,
        categories=[default_category],
    )

    assert results.count == 0


def _test_postgresql_backend_search_searches_threads(
    user_permissions_factory, backend, search_index, user, default_category
):
    user_permissions = user_permissions_factory(user)

    results = backend.search_threads(
        "forum software",
        user_permissions,
        categories=[default_category],
    )

    assert results.count == 1

    result = results.results[0]
    assert result.post_id == ["first_post"].id
    assert result.thread_title == "<hl>Forum</hl> <hl>software</hl> recommendations?"
    assert result.post_content == (
        "I am looking for a good <hl>forum</hl> <hl>software</hl> for my next project."
        " "
        "Any recommendations?"
    )


def _test_postgresql_backend_thread_search_handles_empty_result(
    user_permissions_factory, backend, search_index, user, default_category
):
    user_permissions = user_permissions_factory(user)

    results = backend.search_threads(
        "lorem ipsum",
        user_permissions,
        categories=[default_category],
    )

    assert results.count == 0


def _test_postgresql_backend_search_searches_posts(
    user_permissions_factory, backend, search_index, user, default_category
):
    user_permissions = user_permissions_factory(user)

    results = backend.search_posts(
        "forum software",
        user_permissions,
        categories=[default_category],
    )

    results_ids = [result.post for result in results]
    assert search_index["first_post"].id in results_ids


def _test_postgresql_backend_post_search_handles_empty_result(
    user_permissions_factory, backend, search_index, user, default_category
):
    user_permissions = user_permissions_factory(user)

    results = backend.search_posts(
        "lorem ipsum",
        user_permissions,
        categories=[default_category],
    )

    assert results.count == 0


def test_postgresql_backend_update_thread_first_post_updates_thread_first_post(
    thread_factory, thread_reply_factory, backend, default_category
):
    thread = thread_factory(default_category, title="Lorem ipsum")
    old_first_post = thread.first_post
    new_first_post = thread_reply_factory(thread, content="Hello world")

    backend.index_threads([thread])
    backend.index_posts(
        [
            (old_first_post, old_first_post.content),
            (new_first_post, new_first_post.content),
        ]
    )

    thread.first_post = new_first_post
    thread.save()

    updated = backend.update_thread_first_post(thread)
    assert updated == 2

    old_first_post_index = PostSearch.objects.get(post=old_first_post)
    assert not old_first_post_index.is_first_post

    new_first_post_index = PostSearch.objects.get(post=new_first_post)
    assert new_first_post_index.is_first_post


def test_postgresql_backend_update_thread_first_post_doesnt_update_thread_first_post(
    thread_factory, backend, default_category
):
    thread = thread_factory(default_category, title="Lorem ipsum")
    first_post = thread.first_post

    backend.index_threads([thread])
    backend.index_posts([(first_post, first_post.content)])

    updated = backend.update_thread_first_post(thread)
    assert updated == 0

    first_post_index = PostSearch.objects.get(post=first_post)
    assert first_post_index.is_first_post


def test_postgresql_backend_update_thread_title_updates_thread_and_post_index(
    thread_factory, thread_reply_factory, backend, default_category
):
    thread = thread_factory(default_category, title="Lorem ipsum")
    post = thread_reply_factory(thread, content="Hello world")

    backend.index_threads([thread])
    backend.index_posts([(post, post.content)])

    thread.title = "Dolor met"
    thread.save()

    updated = backend.update_thread_title(thread)
    assert updated == 2

    thread_search = ThreadSearch.objects.get(thread=thread)
    assert thread_search.title == "Dolor met"

    assert ThreadSearch.objects.filter(
        search_vector=SearchQuery("Dolor met", config=backend.search_config),
    ).exists()
    assert PostSearch.objects.filter(
        thread_search_vector=SearchQuery("Dolor met", config=backend.search_config),
    ).exists()

    assert not ThreadSearch.objects.filter(
        search_vector=SearchQuery("Lorem ipsum", config=backend.search_config),
    ).exists()
    assert not PostSearch.objects.filter(
        thread_search_vector=SearchQuery("Lorem ipsum", config=backend.search_config),
    ).exists()


def test_postgresql_backend_update_thread_title_escapes_thread_title(
    thread_factory, backend, default_category
):
    thread = thread_factory(default_category, title="Lorem ipsum")

    backend.index_threads([thread])

    thread.title = "Dolor <b>met</b>"
    thread.save()

    updated = backend.update_thread_title(thread)
    assert updated == 1

    thread_search = ThreadSearch.objects.get(thread=thread)
    assert thread_search.title == "Dolor &lt;b&gt;met&lt;/b&gt;"


def test_postgresql_backend_update_thread_members_is_noop(
    thread_factory, backend, default_category
):
    thread = thread_factory(default_category)

    backend.index_threads([thread])

    updated = backend.update_thread_members(thread, [])
    assert updated == 0


def test_postgresql_backend_update_threads_raises_exception_if_no_filter_is_set(
    thread_factory, backend, default_category, sibling_category
):
    thread = thread_factory(default_category)

    backend.index_threads([thread])

    with pytest.raises(ValueError):
        backend.update_threads({"category": sibling_category})

    thread_search = ThreadSearch.objects.get(thread=thread)
    assert thread_search.category_id == default_category.id


def test_postgresql_backend_update_threads_filters_by_category(
    thread_factory, backend, default_category, sibling_category, other_category
):
    thread = thread_factory(default_category)
    other_thread = thread_factory(other_category)

    backend.index_threads([thread, other_thread])

    updated = backend.update_threads(
        {"category": sibling_category}, categories=[default_category]
    )
    assert updated == 1

    thread_search = ThreadSearch.objects.get(thread=thread)
    assert thread_search.category_id == sibling_category.id

    other_thread_search = ThreadSearch.objects.get(thread=other_thread)
    assert other_thread_search.category_id == other_category.id


def test_postgresql_backend_update_threads_filters_by_thread(
    thread_factory, backend, default_category, sibling_category
):
    thread = thread_factory(default_category)
    other_thread = thread_factory(default_category)

    backend.index_threads([thread, other_thread])

    updated = backend.update_threads({"category": sibling_category}, threads=[thread])
    assert updated == 1

    thread_search = ThreadSearch.objects.get(thread=thread)
    assert thread_search.category_id == sibling_category.id

    other_thread_search = ThreadSearch.objects.get(thread=other_thread)
    assert other_thread_search.category_id == default_category.id


def test_postgresql_backend_update_threads_filters_by_starter(
    thread_factory, backend, user, default_category, sibling_category
):
    thread = thread_factory(default_category, starter=user)
    other_thread = thread_factory(default_category)

    backend.index_threads([thread, other_thread])

    updated = backend.update_threads({"category": sibling_category}, starters=[user])
    assert updated == 1

    thread_search = ThreadSearch.objects.get(thread=thread)
    assert thread_search.category_id == sibling_category.id

    other_thread_search = ThreadSearch.objects.get(thread=other_thread)
    assert other_thread_search.category_id == default_category.id


def test_postgresql_backend_update_threads_updates_thread_category(
    thread_factory, backend, default_category, sibling_category
):
    thread = thread_factory(default_category)
    backend.index_threads([thread])

    updated = backend.update_threads({"category": sibling_category}, threads=[thread])
    assert updated == 1

    thread_search = ThreadSearch.objects.get(thread=thread)
    assert thread_search.category_id == sibling_category.id


def test_postgresql_backend_update_threads_updates_thread_category_id(
    thread_factory, backend, default_category, sibling_category
):
    thread = thread_factory(default_category)
    backend.index_threads([thread])

    updated = backend.update_threads(
        {"category_id": sibling_category.id}, threads=[thread]
    )
    assert updated == 1

    thread_search = ThreadSearch.objects.get(thread=thread)
    assert thread_search.category_id == sibling_category.id


def test_postgresql_backend_update_threads_raises_exception_if_category_and_category_id_is_used_together(
    thread_factory, backend, default_category, sibling_category
):
    thread = thread_factory(default_category)
    backend.index_threads([thread])

    with pytest.raises(ValueError):
        backend.update_threads(
            {"category": sibling_category, "category_id": sibling_category.id},
            threads=[thread],
        )

    thread_search = ThreadSearch.objects.get(thread=thread)
    assert thread_search.category_id == default_category.id


def test_postgresql_backend_update_threads_updates_thread_starter(
    thread_factory, backend, user, default_category
):
    thread = thread_factory(default_category)
    backend.index_threads([thread])

    updated = backend.update_threads({"starter": user}, threads=[thread])
    assert updated == 1

    thread_search = ThreadSearch.objects.get(thread=thread)
    assert thread_search.starter_id == user.id


def test_postgresql_backend_update_threads_updates_thread_starter_id(
    thread_factory, backend, user, default_category
):
    thread = thread_factory(default_category, starter=user)
    backend.index_threads([thread])

    updated = backend.update_threads({"starter_id": user.id}, threads=[thread])
    assert updated == 1

    thread_search = ThreadSearch.objects.get(thread=thread)
    assert thread_search.starter_id == user.id


def test_postgresql_backend_update_threads_raises_exception_if_starter_and_starter_id_is_used_together(
    thread_factory, backend, user, default_category
):
    thread = thread_factory(default_category)
    backend.index_threads([thread])

    with pytest.raises(ValueError):
        backend.update_threads(
            {"starter": user, "starter_id": user.id},
            threads=[thread],
        )

    thread_search = ThreadSearch.objects.get(thread=thread)
    assert thread_search.starter_id is None


def test_postgresql_backend_update_threads_update_is_hidden_is_noop(
    thread_factory, backend, default_category
):
    thread = thread_factory(default_category)
    backend.index_threads([thread])

    updated = backend.update_threads({"is_hidden": True}, threads=[thread])
    assert updated == 0


def test_postgresql_backend_update_threads_update_is_unapproved_is_noop(
    thread_factory, backend, default_category
):
    thread = thread_factory(default_category)
    backend.index_threads([thread])

    updated = backend.update_threads({"is_unapproved": True}, threads=[thread])
    assert updated == 0


def test_postgresql_backend_update_posts_raises_exception_if_no_filter_is_set(
    thread_factory, thread_reply_factory, backend, default_category, sibling_category
):
    thread = thread_factory(default_category)
    post = thread_reply_factory(thread)

    backend.index_threads([thread])
    backend.index_posts([(post, post.content)])

    with pytest.raises(ValueError):
        backend.update_posts({"category": sibling_category})

    thread_search = ThreadSearch.objects.get(thread=thread)
    assert thread_search.category_id == default_category.id

    post_search = PostSearch.objects.get(post=post)
    assert post_search.category_id == default_category.id


def test_postgresql_backend_update_posts_filters_by_category(
    thread_factory,
    thread_reply_factory,
    backend,
    default_category,
    sibling_category,
):
    thread = thread_factory(default_category)
    post = thread_reply_factory(thread)
    other_post = thread_reply_factory(thread)

    backend.index_threads([thread])
    backend.index_posts([(post, post.content), (other_post, other_post.content)])

    updated = backend.update_posts(
        {"category": sibling_category}, categories=[default_category]
    )
    assert updated == 2

    post_search = PostSearch.objects.get(post=post)
    assert post_search.category_id == sibling_category.id

    other_post_search = PostSearch.objects.get(post=other_post)
    assert other_post_search.category_id == sibling_category.id


def test_postgresql_backend_update_posts_filters_by_thread(
    thread_factory,
    thread_reply_factory,
    backend,
    default_category,
    sibling_category,
):
    thread = thread_factory(default_category)
    other_thread = thread_factory(default_category)

    post = thread_reply_factory(thread)
    other_post = thread_reply_factory(other_thread)

    backend.index_threads([thread])
    backend.index_posts([(post, post.content), (other_post, other_post.content)])

    updated = backend.update_posts({"category": sibling_category}, threads=[thread])
    assert updated == 1

    post_search = PostSearch.objects.get(post=post)
    assert post_search.category_id == sibling_category.id

    other_post_search = PostSearch.objects.get(post=other_post)
    assert other_post_search.category_id == default_category.id


def test_postgresql_backend_update_posts_filters_by_post(
    thread_factory,
    thread_reply_factory,
    backend,
    default_category,
    sibling_category,
):
    thread = thread_factory(default_category)
    post = thread_reply_factory(thread)
    other_post = thread_reply_factory(thread)

    backend.index_threads([thread])
    backend.index_posts([(post, post.content), (other_post, other_post.content)])

    updated = backend.update_posts({"category": sibling_category}, posts=[post])
    assert updated == 1

    post_search = PostSearch.objects.get(post=post)
    assert post_search.category_id == sibling_category.id

    other_post_search = PostSearch.objects.get(post=other_post)
    assert other_post_search.category_id == default_category.id


def test_postgresql_backend_update_posts_filters_by_poster(
    thread_factory,
    thread_reply_factory,
    backend,
    user,
    default_category,
    sibling_category,
):
    thread = thread_factory(default_category)
    post = thread_reply_factory(thread, poster=user)
    other_post = thread_reply_factory(thread)

    backend.index_threads([thread])
    backend.index_posts([(post, post.content), (other_post, other_post.content)])

    updated = backend.update_posts({"category": sibling_category}, posters=[user])
    assert updated == 1

    post_search = PostSearch.objects.get(post=post)
    assert post_search.category_id == sibling_category.id

    other_post_search = PostSearch.objects.get(post=other_post)
    assert other_post_search.category_id == default_category.id


def test_postgresql_backend_update_posts_updates_post_category(
    thread_factory,
    thread_reply_factory,
    backend,
    default_category,
    sibling_category,
):
    thread = thread_factory(default_category)
    post = thread_reply_factory(thread)

    backend.index_threads([thread])
    backend.index_posts([(post, post.content)])

    updated = backend.update_posts({"category": sibling_category}, posts=[post])
    assert updated == 1

    post_search = PostSearch.objects.get(post=post)
    assert post_search.category_id == sibling_category.id


def test_postgresql_backend_update_posts_updates_post_category_id(
    thread_factory,
    thread_reply_factory,
    backend,
    default_category,
    sibling_category,
):
    thread = thread_factory(default_category)
    post = thread_reply_factory(thread)

    backend.index_threads([thread])
    backend.index_posts([(post, post.content)])

    updated = backend.update_posts({"category_id": sibling_category.id}, posts=[post])
    assert updated == 1

    post_search = PostSearch.objects.get(post=post)
    assert post_search.category_id == sibling_category.id


def test_postgresql_backend_update_posts_raises_exception_if_category_and_category_id_is_used_together(
    thread_factory,
    thread_reply_factory,
    backend,
    default_category,
    sibling_category,
):
    thread = thread_factory(default_category)
    post = thread_reply_factory(thread)

    backend.index_threads([thread])
    backend.index_posts([(post, post.content)])

    with pytest.raises(ValueError):
        backend.update_posts(
            {"category": sibling_category, "category_id": sibling_category.id},
            posts=[post],
        )

    post_search = PostSearch.objects.get(post=post)
    assert post_search.category_id == default_category.id


def test_postgresql_backend_update_posts_updates_post_thread(
    thread_factory,
    thread_reply_factory,
    backend,
    default_category,
):
    thread = thread_factory(default_category)
    other_thread = thread_factory(default_category)
    post = thread_reply_factory(thread)

    backend.index_threads([thread])
    backend.index_posts([(post, post.content)])

    updated = backend.update_posts({"thread": other_thread}, posts=[post])
    assert updated == 1

    post_search = PostSearch.objects.get(post=post)
    assert post_search.thread_id == other_thread.id


def test_postgresql_backend_update_posts_updates_post_thread_id(
    thread_factory,
    thread_reply_factory,
    backend,
    default_category,
):
    thread = thread_factory(default_category)
    other_thread = thread_factory(default_category)
    post = thread_reply_factory(thread)

    backend.index_threads([thread])
    backend.index_posts([(post, post.content)])

    updated = backend.update_posts({"thread_id": other_thread.id}, posts=[post])
    assert updated == 1

    post_search = PostSearch.objects.get(post=post)
    assert post_search.thread_id == other_thread.id


def test_postgresql_backend_update_posts_raises_exception_if_thread_and_thread_id_is_used_together(
    thread_factory,
    thread_reply_factory,
    backend,
    default_category,
):
    thread = thread_factory(default_category)
    other_thread = thread_factory(default_category)
    post = thread_reply_factory(thread)

    backend.index_threads([thread])
    backend.index_posts([(post, post.content)])

    with pytest.raises(ValueError):
        backend.update_posts(
            {"thread": other_thread, "thread_id": other_thread.id},
            posts=[post],
        )

    post_search = PostSearch.objects.get(post=post)
    assert post_search.thread_id == thread.id


def test_postgresql_backend_update_posts_updates_post_poster(
    thread_factory,
    thread_reply_factory,
    backend,
    user,
    default_category,
):
    thread = thread_factory(default_category)
    post = thread_reply_factory(thread)

    backend.index_threads([thread])
    backend.index_posts([(post, post.content)])

    updated = backend.update_posts({"poster": user}, posts=[post])
    assert updated == 1

    post_search = PostSearch.objects.get(post=post)
    assert post_search.poster_id == user.id


def test_postgresql_backend_update_posts_updates_post_poster_id(
    thread_factory,
    thread_reply_factory,
    backend,
    user,
    default_category,
):
    thread = thread_factory(default_category)
    post = thread_reply_factory(thread)

    backend.index_threads([thread])
    backend.index_posts([(post, post.content)])

    updated = backend.update_posts({"poster_id": user.id}, posts=[post])
    assert updated == 1

    post_search = PostSearch.objects.get(post=post)
    assert post_search.poster_id == user.id


def test_postgresql_backend_update_posts_raises_exception_if_poster_and_poster_id_is_used_together(
    thread_factory,
    thread_reply_factory,
    backend,
    user,
    default_category,
):
    thread = thread_factory(default_category)
    post = thread_reply_factory(thread)

    backend.index_threads([thread])
    backend.index_posts([(post, post.content)])

    with pytest.raises(ValueError):
        backend.update_posts(
            {"poster": user, "poster_id": user.id},
            posts=[post],
        )

    post_search = PostSearch.objects.get(post=post)
    assert post_search.poster_id is None


def test_postgresql_backend_update_posts_update_is_hidden_is_noop(
    thread_factory,
    thread_reply_factory,
    backend,
    default_category,
):
    thread = thread_factory(default_category)
    post = thread_reply_factory(thread)

    backend.index_threads([thread])
    backend.index_posts([(post, post.content)])

    updated = backend.update_posts({"is_hidden": True}, posts=[post])
    assert updated == 0


def test_postgresql_backend_update_posts_update_is_unapproved_is_noop(
    thread_factory,
    thread_reply_factory,
    backend,
    default_category,
):
    thread = thread_factory(default_category)
    post = thread_reply_factory(thread)

    backend.index_threads([thread])
    backend.index_posts([(post, post.content)])

    updated = backend.update_posts({"is_unapproved": True}, posts=[post])
    assert updated == 0


def test_postgresql_backend_delete_deletes_all_threads_and_posts_in_category(
    thread_factory, thread_reply_factory, backend, default_category, sibling_category
):
    thread = thread_factory(default_category)
    other_thread = thread_factory(sibling_category)

    post = thread_reply_factory(thread)
    other_post = thread_reply_factory(other_thread)

    backend.index_threads([thread, other_thread])
    backend.index_posts([(post, post.content), (other_post, other_post.content)])

    deleted = backend.delete(categories=[default_category])
    assert deleted == 2

    with pytest.raises(ThreadSearch.DoesNotExist):
        ThreadSearch.objects.get(thread=thread)

    with pytest.raises(PostSearch.DoesNotExist):
        PostSearch.objects.get(post=post)

    ThreadSearch.objects.get(thread=other_thread)
    PostSearch.objects.get(post=other_post)


def test_postgresql_backend_delete_deletes_all_threads_and_posts_in_thread(
    thread_factory, thread_reply_factory, backend, default_category, sibling_category
):
    thread = thread_factory(default_category)
    other_thread = thread_factory(sibling_category)

    post = thread_reply_factory(thread)
    other_post = thread_reply_factory(other_thread)

    backend.index_threads([thread, other_thread])
    backend.index_posts([(post, post.content), (other_post, other_post.content)])

    deleted = backend.delete(threads=[thread])
    assert deleted == 2

    with pytest.raises(ThreadSearch.DoesNotExist):
        ThreadSearch.objects.get(thread=thread)

    with pytest.raises(PostSearch.DoesNotExist):
        PostSearch.objects.get(post=post)

    ThreadSearch.objects.get(thread=other_thread)
    PostSearch.objects.get(post=other_post)


def test_postgresql_backend_delete_posts(
    thread_factory,
    thread_reply_factory,
    backend,
    user,
    default_category,
    sibling_category,
):
    thread = thread_factory(default_category, starter=user)
    other_thread = thread_factory(sibling_category)

    post = thread_reply_factory(thread)
    other_post = thread_reply_factory(other_thread, poster=user)

    backend.index_threads([thread, other_thread])
    backend.index_posts([(post, post.content), (other_post, other_post.content)])

    deleted = backend.delete(posts=[other_post])
    assert deleted == 1

    with pytest.raises(PostSearch.DoesNotExist):
        PostSearch.objects.get(post=other_post)

    ThreadSearch.objects.get(thread=thread)
    ThreadSearch.objects.get(thread=other_thread)
    PostSearch.objects.get(post=post)


def test_postgresql_backend_delete_deletes_all_threads_and_posts_by_user(
    thread_factory,
    thread_reply_factory,
    backend,
    user,
    default_category,
    sibling_category,
):
    thread = thread_factory(default_category, starter=user)
    other_thread = thread_factory(sibling_category)

    post = thread_reply_factory(thread)
    other_post = thread_reply_factory(other_thread, poster=user)

    backend.index_threads([thread, other_thread])
    backend.index_posts([(post, post.content), (other_post, other_post.content)])

    deleted = backend.delete(users=[user])
    assert deleted == 2

    with pytest.raises(ThreadSearch.DoesNotExist):
        ThreadSearch.objects.get(thread=thread)

    with pytest.raises(PostSearch.DoesNotExist):
        PostSearch.objects.get(post=other_post)

    ThreadSearch.objects.get(thread=other_thread)
    PostSearch.objects.get(post=post)


def test_postgresql_backend_clear_deletes_all_threads_and_posts(
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
