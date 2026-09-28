import pytest

from ..models import PostSearch, ThreadSearch
from ..service import search


def test_search_service_index_thread_indexes_thread(thread_factory, default_category):
    thread = thread_factory(default_category)

    search.index_thread(thread)

    ThreadSearch.objects.get(thread=thread, starter=None)


def test_search_service_bulk_index_threads_indexes_multiple_threads(
    thread_factory, default_category, other_category
):
    thread = thread_factory(default_category)
    other_thread = thread_factory(other_category)

    search.bulk_index_threads([thread, other_thread])

    ThreadSearch.objects.get(thread=thread)
    ThreadSearch.objects.get(thread=other_thread)


def test_search_service_index_post_indexes_post(thread_reply_factory, thread):
    post = thread_reply_factory(thread)

    search.bulk_index_posts([(post, post.content)])

    PostSearch.objects.get(post=post)


def test_search_service_bulk_index_posts_indexes_multiple_post(
    thread_reply_factory, thread
):
    post = thread_reply_factory(thread)
    other_post = thread_reply_factory(thread)

    search.bulk_index_posts(
        [
            (post, post.content),
            (other_post, other_post.content),
        ]
    )

    PostSearch.objects.get(post=post)
    PostSearch.objects.get(post=other_post)


def test_search_service_update_thread_members_updates_members(
    mocker, thread, user, other_user
):
    # We are using a mock because default search backend doesn't implement this
    mock_update_thread_members = mocker.patch(
        "misago.search.service.search.update_thread_members", autospec=True
    )

    search.update_thread_members(thread, [user.id, other_user.id])

    mock_update_thread_members.assert_called_with(thread, [user.id, other_user.id])


def test_search_service_move_category_data_updates_related_search_data(
    thread_factory,
    thread_reply_factory,
    default_category,
    sibling_category,
    other_category,
):
    thread = thread_factory(default_category)
    other_thread = thread_factory(other_category)

    post = thread_reply_factory(thread)
    other_post = thread_reply_factory(other_thread)

    search.bulk_index_threads([thread, other_thread])
    search.bulk_index_posts(
        [
            (post, post.content),
            (other_post, other_post.content),
        ]
    )

    ThreadSearch.objects.get(thread=thread, category=default_category)
    PostSearch.objects.get(post=post, category=default_category)

    ThreadSearch.objects.get(thread=other_thread, category=other_category)
    PostSearch.objects.get(post=other_post, category=other_category)

    search.move_category_data(default_category, sibling_category)

    ThreadSearch.objects.get(thread=thread, category=sibling_category)
    PostSearch.objects.get(post=post, category=sibling_category)

    ThreadSearch.objects.get(thread=other_thread, category=other_category)
    PostSearch.objects.get(post=other_post, category=other_category)


def test_search_service_bulk_move_categories_data_updates_related_search_data(
    thread_factory,
    thread_reply_factory,
    default_category,
    sibling_category,
    other_category,
):
    thread = thread_factory(default_category)
    other_thread = thread_factory(sibling_category)

    post = thread_reply_factory(thread)
    other_post = thread_reply_factory(other_thread)

    search.bulk_index_threads([thread, other_thread])
    search.bulk_index_posts(
        [
            (post, post.content),
            (other_post, other_post.content),
        ]
    )

    ThreadSearch.objects.get(thread=thread, category=default_category)
    PostSearch.objects.get(post=post, category=default_category)

    ThreadSearch.objects.get(thread=other_thread, category=sibling_category)
    PostSearch.objects.get(post=other_post, category=sibling_category)

    search.bulk_move_categories_data(
        [default_category, sibling_category], other_category
    )

    ThreadSearch.objects.get(thread=thread, category=other_category)
    PostSearch.objects.get(post=post, category=other_category)

    ThreadSearch.objects.get(thread=other_thread, category=other_category)
    PostSearch.objects.get(post=other_post, category=other_category)


def test_search_service_delete_category_data_deletes_related_search_data(
    thread_factory, thread_reply_factory, default_category, sibling_category
):
    thread = thread_factory(default_category)
    other_thread = thread_factory(sibling_category)

    post = thread_reply_factory(thread)
    other_post = thread_reply_factory(other_thread)

    search.bulk_index_threads([thread, other_thread])
    search.bulk_index_posts(
        [
            (post, post.content),
            (other_post, other_post.content),
        ]
    )

    ThreadSearch.objects.get(thread=thread)
    PostSearch.objects.get(post=post)

    ThreadSearch.objects.get(thread=other_thread)
    PostSearch.objects.get(post=other_post)

    search.delete_category_data(sibling_category)

    ThreadSearch.objects.get(thread=thread)
    PostSearch.objects.get(post=post)

    with pytest.raises(ThreadSearch.DoesNotExist):
        ThreadSearch.objects.get(thread=other_thread)

    with pytest.raises(PostSearch.DoesNotExist):
        PostSearch.objects.get(post=other_post)


def test_search_service_bulk_delete_categories_data_deletes_related_search_data(
    thread_factory, thread_reply_factory, default_category, sibling_category
):
    thread = thread_factory(default_category)
    other_thread = thread_factory(sibling_category)

    post = thread_reply_factory(thread)
    other_post = thread_reply_factory(other_thread)

    search.bulk_index_threads([thread, other_thread])
    search.bulk_index_posts(
        [
            (post, post.content),
            (other_post, other_post.content),
        ]
    )

    ThreadSearch.objects.get(thread=thread)
    PostSearch.objects.get(post=post)

    ThreadSearch.objects.get(thread=other_thread)
    PostSearch.objects.get(post=other_post)

    search.bulk_delete_categories_data([default_category, sibling_category])

    with pytest.raises(ThreadSearch.DoesNotExist):
        ThreadSearch.objects.get(thread=thread)

    with pytest.raises(ThreadSearch.DoesNotExist):
        ThreadSearch.objects.get(thread=other_thread)

    with pytest.raises(PostSearch.DoesNotExist):
        PostSearch.objects.get(post=post)

    with pytest.raises(PostSearch.DoesNotExist):
        PostSearch.objects.get(post=other_post)


def test_search_service_clear_deletes_all_search_data(
    thread_factory, thread_reply_factory, default_category
):
    thread = thread_factory(default_category)
    other_thread = thread_factory(default_category)

    post = thread_reply_factory(thread)
    other_post = thread_reply_factory(other_thread)

    search.bulk_index_threads([thread, other_thread])
    search.bulk_index_posts(
        [
            (post, post.content),
            (other_post, other_post.content),
        ]
    )

    assert ThreadSearch.objects.exists()
    assert PostSearch.objects.exists()

    search.clear()

    assert not ThreadSearch.objects.exists()
    assert not PostSearch.objects.exists()
