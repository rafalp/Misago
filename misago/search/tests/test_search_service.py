from datetime import timedelta

import pytest
from django.utils import timezone

from ..enums import SearchMode, SearchSort
from ..models import PostSearch, ThreadSearch
from ..query import parse_search_query
from ..service import search


def test_search_service_search_threads_delegates_call_to_backend(
    mocker, user_permissions, user, default_category, thread
):
    mock_search_threads = mocker.patch.object(
        search.backend,
        "search_threads",
        autospec=True,
        return_value=[1, 3, 4],
    )

    search_query = parse_search_query("lorem ipsum")
    after = timezone.now() - timedelta(minutes=60)
    before = timezone.now() - timedelta(minutes=30)

    result = search.search_threads(
        search_query,
        user_permissions,
        categories=[default_category],
        threads=[thread],
        users=[user],
        after=after,
        before=before,
        mode=SearchMode.POSTS,
        order_by=SearchSort.NEWEST,
        offset=50,
        limit=20,
        extra=True,
    )

    assert result == [1, 3, 4]

    mock_search_threads.assert_called_once_with(
        search_query,
        user_permissions,
        categories=[default_category],
        threads=[thread],
        users=[user],
        after=after,
        before=before,
        mode=SearchMode.POSTS,
        order_by=SearchSort.NEWEST,
        offset=50,
        limit=20,
        extra=True,
    )


def test_search_service_search_private_threads_delegates_call_to_backend(
    mocker, user_permissions, user, thread
):
    mock_search_private_threads = mocker.patch.object(
        search.backend,
        "search_private_threads",
        autospec=True,
        return_value=[1, 3, 4],
    )

    search_query = parse_search_query("lorem ipsum")
    after = timezone.now() - timedelta(minutes=60)
    before = timezone.now() - timedelta(minutes=30)

    result = search.search_private_threads(
        search_query,
        user_permissions,
        threads=[thread],
        users=[user],
        after=after,
        before=before,
        mode=SearchMode.POSTS,
        order_by=SearchSort.NEWEST,
        offset=50,
        limit=20,
        extra=True,
    )

    assert result == [1, 3, 4]

    mock_search_private_threads.assert_called_once_with(
        search_query,
        user_permissions,
        threads=[thread],
        users=[user],
        after=after,
        before=before,
        mode=SearchMode.POSTS,
        order_by=SearchSort.NEWEST,
        offset=50,
        limit=20,
        extra=True,
    )


def test_search_service_index_thread_delegates_call_to_backend(mocker, thread):
    mock_index_threads = mocker.patch.object(
        search.backend,
        "index_threads",
        autospec=True,
        return_value=1,
    )

    assert search.index_thread(thread) == 1
    mock_index_threads.assert_called_once_with([thread])


def test_search_service_bulk_index_threads_delegates_call_to_backend(
    mocker, thread, user_thread
):
    mock_index_threads = mocker.patch.object(
        search.backend,
        "index_threads",
        autospec=True,
        return_value=2,
    )

    assert search.bulk_index_threads([thread, user_thread]) == 2
    mock_index_threads.assert_called_once_with([thread, user_thread])


def test_search_service_index_post_delegates_call_to_backend(mocker, post):
    mock_index_posts = mocker.patch.object(
        search.backend,
        "index_posts",
        autospec=True,
        return_value=1,
    )

    assert search.index_post(post, "Search document") == 1
    mock_index_posts.assert_called_once_with([(post, "Search document")])


def test_search_service_bulk_index_posts_delegates_call_to_backend(mocker, post, reply):
    mock_index_posts = mocker.patch.object(
        search.backend,
        "index_posts",
        autospec=True,
        return_value=2,
    )

    assert (
        search.bulk_index_posts(
            [
                (post, "Search document 1"),
                (reply, "Search document 2"),
            ]
        )
        == 2
    )

    mock_index_posts.assert_called_once_with(
        [
            (post, "Search document 1"),
            (reply, "Search document 2"),
        ]
    )


def test_search_service_update_thread_first_post_delegates_call_to_backend(
    mocker, thread
):
    mock_update_thread_first_post = mocker.patch.object(
        search.backend,
        "update_thread_first_post",
        autospec=True,
        return_value=1,
    )

    assert search.update_thread_first_post(thread) == 1
    mock_update_thread_first_post.assert_called_once_with(thread)


def test_search_service_update_thread_title_delegates_call_to_backend(mocker, thread):
    mock_update_thread_title = mocker.patch.object(
        search.backend,
        "update_thread_title",
        autospec=True,
        return_value=1,
    )

    assert search.update_thread_title(thread) == 1
    mock_update_thread_title.assert_called_once_with(thread)


def test_search_service_update_thread_members_delegates_call_to_backend(
    mocker, thread, user, other_user
):
    # We are using a mock because in default search backend this is noop
    mock_update_thread_members = mocker.patch.object(
        search.backend,
        "update_thread_members",
        autospec=True,
        return_value=12,
    )

    assert search.update_thread_members(thread, [user.id, other_user.id]) == 12
    mock_update_thread_members.assert_called_once_with(thread, [user.id, other_user.id])


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


def test_search_service_delete_category_data_delegates_call_to_backend(
    mocker, default_category
):
    mock_delete = mocker.patch.object(
        search.backend,
        "delete",
        autospec=True,
        return_value=12,
    )

    assert search.delete_category_data(default_category) == 12
    mock_delete.assert_called_once_with(categories=[default_category])


def test_search_service_bulk_delete_categories_data_delegates_call_to_backend(
    mocker, default_category, sibling_category
):
    mock_delete = mocker.patch.object(
        search.backend,
        "delete",
        autospec=True,
        return_value=12,
    )

    assert (
        search.bulk_delete_categories_data(
            [
                default_category,
                sibling_category,
            ]
        )
        == 12
    )

    mock_delete.assert_called_once_with(
        categories=[
            default_category,
            sibling_category,
        ]
    )


def test_search_service_clear_delegates_call_to_backend(mocker):
    mock_clear = mocker.patch.object(
        search.backend,
        "clear",
        autospec=True,
        return_value=1,
    )

    assert search.clear() == 1
    mock_clear.assert_called_once_with()
