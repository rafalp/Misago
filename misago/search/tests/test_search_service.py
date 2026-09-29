from datetime import timedelta

import pytest
from django.utils import timezone

from ...permissions.enums import CategoryPermission
from ...privatethreads.models import PrivateThreadMember
from ...testutils import grant_category_group_permissions
from ...threads.synchronize import synchronize_thread
from ..enums import SearchMode, SearchSort
from ..models import PostSearch, ThreadSearch
from ..query import parse_search_query
from ..service import search


@pytest.mark.parametrize("order_by", SearchSort)
def test_search_service_search_threads_searches_threads(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
    order_by,
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

    search.bulk_index_threads([databases_thread, cars_thread])
    search.bulk_index_posts(
        [
            (mysql_post, "MySQL is OpenSource and widely available."),
            (postgresql_post, "PostgreSQL has great features!"),
            (seat_post, "I love SEAT"),
            (nissan_post, "I drive Nissan"),
        ]
    )

    user_permissions = user_permissions_factory(user)

    results = search.search_threads(
        parse_search_query("postgresql database"),
        user_permissions,
        categories=[default_category],
        order_by=order_by,
    )

    assert len(results.items) == 1
    assert results.items[0].post_id == postgresql_post.id
    assert results.items[0].thread_title == (
        "<strong>Database</strong> engine recommendation"
    )
    assert results.items[0].post_content == (
        "<strong>PostgreSQL</strong> has great features!"
    )


@pytest.mark.parametrize("order_by", SearchSort)
def test_search_service_search_threads_searches_posts(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
    order_by,
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

    search.bulk_index_threads([databases_thread, cars_thread])
    search.bulk_index_posts(
        [
            (mysql_post, "MySQL is OpenSource and widely available."),
            (postgresql_post, "PostgreSQL has great features!"),
            (seat_post, "I love SEAT"),
            (nissan_post, "I drive Nissan"),
        ]
    )

    user_permissions = user_permissions_factory(user)

    results = search.search_threads(
        parse_search_query("seat"),
        user_permissions,
        categories=[default_category],
        mode=SearchMode.POSTS,
        order_by=order_by,
    )

    assert len(results.items) == 1
    assert results.items[0].post_id == seat_post.id
    assert results.items[0].thread_title == "Favorite car?"
    assert results.items[0].post_content == "I love <strong>SEAT</strong>"


@pytest.mark.parametrize("order_by", SearchSort)
def test_search_service_search_threads_searches_thread_titles(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
    order_by,
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

    search.bulk_index_threads([databases_thread, cars_thread])
    search.bulk_index_posts(
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

    results = search.search_threads(
        parse_search_query("database"),
        user_permissions,
        categories=[default_category],
        mode=SearchMode.THREAD_TITLES,
        order_by=order_by,
    )

    assert len(results.items) == 1
    assert results.items[0].post_id == databases_post.id
    assert results.items[0].thread_title == (
        "<strong>Database</strong> engine recommendation"
    )
    assert results.items[0].post_content == "What are you using?"


@pytest.mark.parametrize("order_by", SearchSort)
def test_search_service_search_private_threads_searches_threads(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    private_threads_category,
    order_by,
):
    databases_thread = thread_factory(
        private_threads_category, title="Database engine recommendation"
    )
    databases_post = databases_thread.first_post
    mysql_post = thread_reply_factory(databases_thread)
    postgresql_post = thread_reply_factory(databases_thread)

    cars_thread = thread_factory(private_threads_category, title="Favorite car?")
    seat_post = thread_reply_factory(cars_thread)
    nissan_post = thread_reply_factory(cars_thread)

    synchronize_thread(databases_thread)
    synchronize_thread(cars_thread)

    PrivateThreadMember.objects.create(thread=databases_thread, user=user)
    PrivateThreadMember.objects.create(thread=cars_thread, user=user)

    search.bulk_index_threads([databases_thread, cars_thread])
    search.bulk_index_posts(
        [
            (databases_post, "What are you using?"),
            (mysql_post, "MySQL is OpenSource and widely available."),
            (postgresql_post, "PostgreSQL has great features!"),
            (seat_post, "I love SEAT"),
            (nissan_post, "I drive Nissan"),
        ]
    )

    user_permissions = user_permissions_factory(user)

    results = search.search_private_threads(
        parse_search_query("postgresql database"),
        user_permissions,
        order_by=order_by,
    )

    assert len(results.items) == 1
    assert results.items[0].post_id == postgresql_post.id
    assert results.items[0].thread_title == (
        "<strong>Database</strong> engine recommendation"
    )
    assert results.items[0].post_content == (
        "<strong>PostgreSQL</strong> has great features!"
    )


@pytest.mark.parametrize("order_by", SearchSort)
def test_search_service_search_private_threads_searches_posts(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    private_threads_category,
    order_by,
):
    databases_thread = thread_factory(
        private_threads_category, title="Database engine recommendation"
    )
    mysql_post = thread_reply_factory(databases_thread)
    postgresql_post = thread_reply_factory(databases_thread)

    cars_thread = thread_factory(private_threads_category, title="Favorite car?")
    seat_post = thread_reply_factory(cars_thread)
    nissan_post = thread_reply_factory(cars_thread)

    synchronize_thread(databases_thread)
    synchronize_thread(cars_thread)

    PrivateThreadMember.objects.create(thread=databases_thread, user=user)
    PrivateThreadMember.objects.create(thread=cars_thread, user=user)

    search.bulk_index_threads([databases_thread, cars_thread])
    search.bulk_index_posts(
        [
            (mysql_post, "MySQL is OpenSource and widely available."),
            (postgresql_post, "PostgreSQL has great features!"),
            (seat_post, "I love SEAT"),
            (nissan_post, "I drive Nissan"),
        ]
    )

    user_permissions = user_permissions_factory(user)

    results = search.search_private_threads(
        parse_search_query("seat"),
        user_permissions,
        mode=SearchMode.POSTS,
        order_by=order_by,
    )

    assert len(results.items) == 1
    assert results.items[0].post_id == seat_post.id
    assert results.items[0].thread_title == "Favorite car?"
    assert results.items[0].post_content == "I love <strong>SEAT</strong>"


@pytest.mark.parametrize("order_by", SearchSort)
def test_search_service_search_private_threads_searches_thread_titles(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    private_threads_category,
    order_by,
):
    databases_thread = thread_factory(
        private_threads_category, title="Database engine recommendation"
    )
    databases_post = databases_thread.first_post
    mysql_post = thread_reply_factory(databases_thread)
    postgresql_post = thread_reply_factory(databases_thread)

    cars_thread = thread_factory(private_threads_category, title="Favorite car?")
    cars_post = cars_thread.first_post
    seat_post = thread_reply_factory(cars_thread)
    nissan_post = thread_reply_factory(cars_thread)

    synchronize_thread(databases_thread)
    synchronize_thread(cars_thread)

    PrivateThreadMember.objects.create(thread=databases_thread, user=user)
    PrivateThreadMember.objects.create(thread=cars_thread, user=user)

    search.bulk_index_threads([databases_thread, cars_thread])
    search.bulk_index_posts(
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

    results = search.search_private_threads(
        parse_search_query("database"),
        user_permissions,
        mode=SearchMode.THREAD_TITLES,
        order_by=order_by,
    )

    assert len(results.items) == 1
    assert results.items[0].post_id == databases_post.id
    assert results.items[0].thread_title == (
        "<strong>Database</strong> engine recommendation"
    )
    assert results.items[0].post_content == "What are you using?"


@pytest.mark.parametrize("search_mode", SearchMode)
def test_search_service_search_threads_filters_by_category(
    thread_factory,
    user_permissions_factory,
    user,
    default_category,
    sibling_category,
    search_mode,
):
    thread = thread_factory(default_category, title="Title ipsum dolor")
    post = thread.first_post

    other_thread = thread_factory(sibling_category, title="Title ipsum dolor")
    other_post = other_thread.first_post

    search.bulk_index_threads([thread, other_thread])
    search.bulk_index_posts(
        [
            (post, "Post ipsum dolor"),
            (other_post, "Post ipsum dolor"),
        ]
    )

    grant_category_group_permissions(
        sibling_category, user.group, CategoryPermission.SEE, CategoryPermission.BROWSE
    )

    user_permissions = user_permissions_factory(user)

    results = search.search_threads(
        parse_search_query("ipsum"),
        user_permissions,
        categories=[sibling_category],
        mode=search_mode,
    )

    assert len(results.items) == 1
    assert results.items[0].post_id == other_post.id
    assert results.items[0].thread_title == "Title <strong>ipsum</strong> dolor"
    assert results.items[0].post_content == "Post <strong>ipsum</strong> dolor"


@pytest.mark.parametrize("search_mode", SearchMode)
def test_search_service_search_threads_filters_by_thread(
    thread_factory,
    user_permissions_factory,
    user,
    default_category,
    search_mode,
):
    thread = thread_factory(default_category, title="Title ipsum dolor")
    post = thread.first_post

    other_thread = thread_factory(default_category, title="Title ipsum dolor")
    other_post = other_thread.first_post

    search.bulk_index_threads([thread, other_thread])
    search.bulk_index_posts(
        [
            (post, "Post ipsum dolor"),
            (other_post, "Post ipsum dolor"),
        ]
    )

    user_permissions = user_permissions_factory(user)

    results = search.search_threads(
        parse_search_query("ipsum"),
        user_permissions,
        categories=[default_category],
        threads=[other_thread],
        mode=search_mode,
    )

    assert len(results.items) == 1
    assert results.items[0].post_id == other_post.id
    assert results.items[0].thread_title == "Title <strong>ipsum</strong> dolor"
    assert results.items[0].post_content == "Post <strong>ipsum</strong> dolor"


@pytest.mark.parametrize("search_mode", SearchMode)
def test_search_service_search_private_threads_filters_by_thread(
    thread_factory,
    user_permissions_factory,
    user,
    private_threads_category,
    search_mode,
):
    thread = thread_factory(private_threads_category, title="Title ipsum dolor")
    post = thread.first_post

    other_thread = thread_factory(private_threads_category, title="Title ipsum dolor")
    other_post = other_thread.first_post

    PrivateThreadMember.objects.create(thread=thread, user=user)
    PrivateThreadMember.objects.create(thread=other_thread, user=user)

    search.bulk_index_threads([thread, other_thread])
    search.bulk_index_posts(
        [
            (post, "Post ipsum dolor"),
            (other_post, "Post ipsum dolor"),
        ]
    )

    user_permissions = user_permissions_factory(user)

    results = search.search_private_threads(
        parse_search_query("ipsum"),
        user_permissions,
        threads=[other_thread],
        mode=search_mode,
    )

    assert len(results.items) == 1
    assert results.items[0].post_id == other_post.id
    assert results.items[0].thread_title == "Title <strong>ipsum</strong> dolor"
    assert results.items[0].post_content == "Post <strong>ipsum</strong> dolor"


@pytest.mark.parametrize("search_mode", SearchMode)
def test_search_service_search_threads_filters_by_user(
    thread_factory,
    user_permissions_factory,
    user,
    other_user,
    default_category,
    search_mode,
):
    thread = thread_factory(default_category, title="Title ipsum dolor")
    post = thread.first_post

    user_thread = thread_factory(
        default_category, title="Title ipsum dolor", starter=user
    )
    user_post = user_thread.first_post

    other_user_thread = thread_factory(
        default_category, title="Title ipsum dolor", starter=other_user
    )
    other_user_post = other_user_thread.first_post

    search.bulk_index_threads([thread, user_thread, other_user_thread])
    search.bulk_index_posts(
        [
            (post, "Post ipsum dolor"),
            (user_post, "Post ipsum dolor"),
            (other_user_post, "Post ipsum dolor"),
        ]
    )

    user_permissions = user_permissions_factory(user)

    results = search.search_threads(
        parse_search_query("ipsum"),
        user_permissions,
        categories=[default_category],
        users=[other_user],
        mode=search_mode,
    )

    assert len(results.items) == 1
    assert results.items[0].post_id == other_user_post.id
    assert results.items[0].thread_title == "Title <strong>ipsum</strong> dolor"
    assert results.items[0].post_content == "Post <strong>ipsum</strong> dolor"


@pytest.mark.parametrize("search_mode", SearchMode)
def test_search_service_search_private_threads_filters_by_user(
    thread_factory,
    user_permissions_factory,
    user,
    other_user,
    private_threads_category,
    search_mode,
):
    thread = thread_factory(private_threads_category, title="Title ipsum dolor")
    post = thread.first_post

    user_thread = thread_factory(
        private_threads_category, title="Title ipsum dolor", starter=user
    )
    user_post = user_thread.first_post

    other_user_thread = thread_factory(
        private_threads_category, title="Title ipsum dolor", starter=other_user
    )
    other_user_post = other_user_thread.first_post

    PrivateThreadMember.objects.create(thread=thread, user=user)
    PrivateThreadMember.objects.create(thread=user_thread, user=user)
    PrivateThreadMember.objects.create(thread=other_user_thread, user=user)

    search.bulk_index_threads([thread, user_thread, other_user_thread])
    search.bulk_index_posts(
        [
            (post, "Post ipsum dolor"),
            (user_post, "Post ipsum dolor"),
            (other_user_post, "Post ipsum dolor"),
        ]
    )

    user_permissions = user_permissions_factory(user)

    results = search.search_private_threads(
        parse_search_query("ipsum"),
        user_permissions,
        users=[other_user],
        mode=search_mode,
    )

    assert len(results.items) == 1
    assert results.items[0].post_id == other_user_post.id
    assert results.items[0].thread_title == "Title <strong>ipsum</strong> dolor"
    assert results.items[0].post_content == "Post <strong>ipsum</strong> dolor"


@pytest.mark.parametrize("search_mode", SearchMode)
def test_search_service_search_threads_filters_after_date(
    thread_factory,
    user_permissions_factory,
    user,
    default_category,
    search_mode,
):
    thread = thread_factory(
        default_category, title="Title ipsum dolor", started_at=-3600
    )
    post = thread.first_post

    other_thread = thread_factory(default_category, title="Title ipsum dolor")
    other_post = other_thread.first_post

    search.bulk_index_threads([thread, other_thread])
    search.bulk_index_posts(
        [
            (post, "Post ipsum dolor"),
            (other_post, "Post ipsum dolor"),
        ]
    )

    user_permissions = user_permissions_factory(user)

    results = search.search_threads(
        parse_search_query("ipsum"),
        user_permissions,
        categories=[default_category],
        after=timezone.now() - timedelta(minutes=5),
        mode=search_mode,
    )

    assert len(results.items) == 1
    assert results.items[0].post_id == other_post.id
    assert results.items[0].thread_title == "Title <strong>ipsum</strong> dolor"
    assert results.items[0].post_content == "Post <strong>ipsum</strong> dolor"


@pytest.mark.parametrize("search_mode", SearchMode)
def test_search_service_search_private_threads_filters_after_date(
    thread_factory,
    user_permissions_factory,
    user,
    private_threads_category,
    search_mode,
):
    thread = thread_factory(
        private_threads_category, title="Title ipsum dolor", started_at=-3600
    )
    post = thread.first_post

    other_thread = thread_factory(private_threads_category, title="Title ipsum dolor")
    other_post = other_thread.first_post

    PrivateThreadMember.objects.create(thread=thread, user=user)
    PrivateThreadMember.objects.create(thread=other_thread, user=user)

    search.bulk_index_threads([thread, other_thread])
    search.bulk_index_posts(
        [
            (post, "Post ipsum dolor"),
            (other_post, "Post ipsum dolor"),
        ]
    )

    user_permissions = user_permissions_factory(user)

    results = search.search_private_threads(
        parse_search_query("ipsum"),
        user_permissions,
        after=timezone.now() - timedelta(minutes=5),
        mode=search_mode,
    )

    assert len(results.items) == 1
    assert results.items[0].post_id == other_post.id
    assert results.items[0].thread_title == "Title <strong>ipsum</strong> dolor"
    assert results.items[0].post_content == "Post <strong>ipsum</strong> dolor"


@pytest.mark.parametrize("search_mode", SearchMode)
def test_search_service_search_threads_filters_before_date(
    thread_factory,
    user_permissions_factory,
    user,
    default_category,
    search_mode,
):
    thread = thread_factory(
        default_category, title="Title ipsum dolor", started_at=-3600
    )
    post = thread.first_post

    other_thread = thread_factory(default_category, title="Title ipsum dolor")
    other_post = other_thread.first_post

    search.bulk_index_threads([thread, other_thread])
    search.bulk_index_posts(
        [
            (post, "Post ipsum dolor"),
            (other_post, "Post ipsum dolor"),
        ]
    )

    user_permissions = user_permissions_factory(user)

    results = search.search_threads(
        parse_search_query("ipsum"),
        user_permissions,
        categories=[default_category],
        before=timezone.now() - timedelta(minutes=5),
        mode=search_mode,
    )

    assert len(results.items) == 1
    assert results.items[0].post_id == post.id
    assert results.items[0].thread_title == "Title <strong>ipsum</strong> dolor"
    assert results.items[0].post_content == "Post <strong>ipsum</strong> dolor"


@pytest.mark.parametrize("search_mode", SearchMode)
def test_search_service_search_private_threads_filters_before_date(
    thread_factory,
    user_permissions_factory,
    user,
    private_threads_category,
    search_mode,
):
    thread = thread_factory(
        private_threads_category, title="Title ipsum dolor", started_at=-3600
    )
    post = thread.first_post

    other_thread = thread_factory(private_threads_category, title="Title ipsum dolor")
    other_post = other_thread.first_post

    PrivateThreadMember.objects.create(thread=thread, user=user)
    PrivateThreadMember.objects.create(thread=other_thread, user=user)

    search.bulk_index_threads([thread, other_thread])
    search.bulk_index_posts(
        [
            (post, "Post ipsum dolor"),
            (other_post, "Post ipsum dolor"),
        ]
    )

    user_permissions = user_permissions_factory(user)

    results = search.search_private_threads(
        parse_search_query("ipsum"),
        user_permissions,
        before=timezone.now() - timedelta(minutes=5),
        mode=search_mode,
    )

    assert len(results.items) == 1
    assert results.items[0].post_id == post.id
    assert results.items[0].thread_title == "Title <strong>ipsum</strong> dolor"
    assert results.items[0].post_content == "Post <strong>ipsum</strong> dolor"


@pytest.mark.parametrize("search_mode", SearchMode)
def test_search_service_search_threads_filters_between_dates(
    thread_factory,
    user_permissions_factory,
    user,
    default_category,
    search_mode,
):
    thread = thread_factory(
        default_category, title="Title ipsum dolor", started_at=-3600
    )
    post = thread.first_post

    other_thread = thread_factory(
        default_category, title="Title ipsum dolor", started_at=-600
    )
    other_post = other_thread.first_post

    recent_thread = thread_factory(default_category, title="Title ipsum dolor")
    recent_post = recent_thread.first_post

    search.bulk_index_threads([thread, other_thread, recent_thread])
    search.bulk_index_posts(
        [
            (post, "Post ipsum dolor"),
            (other_post, "Post ipsum dolor"),
            (recent_post, "Post ipsum dolor"),
        ]
    )

    user_permissions = user_permissions_factory(user)

    results = search.search_threads(
        parse_search_query("ipsum"),
        user_permissions,
        categories=[default_category],
        after=timezone.now() - timedelta(minutes=15),
        before=timezone.now() - timedelta(minutes=5),
        mode=search_mode,
    )

    assert len(results.items) == 1
    assert results.items[0].post_id == other_post.id
    assert results.items[0].thread_title == "Title <strong>ipsum</strong> dolor"
    assert results.items[0].post_content == "Post <strong>ipsum</strong> dolor"


@pytest.mark.parametrize("search_mode", SearchMode)
def test_search_service_search_private_threads_filters_between_dates(
    thread_factory,
    user_permissions_factory,
    user,
    private_threads_category,
    search_mode,
):
    thread = thread_factory(
        private_threads_category, title="Title ipsum dolor", started_at=-3600
    )
    post = thread.first_post

    other_thread = thread_factory(
        private_threads_category, title="Title ipsum dolor", started_at=-600
    )
    other_post = other_thread.first_post

    recent_thread = thread_factory(private_threads_category, title="Title ipsum dolor")
    recent_post = recent_thread.first_post

    PrivateThreadMember.objects.create(thread=thread, user=user)
    PrivateThreadMember.objects.create(thread=other_thread, user=user)
    PrivateThreadMember.objects.create(thread=recent_thread, user=user)

    search.bulk_index_threads([thread, other_thread, recent_thread])
    search.bulk_index_posts(
        [
            (post, "Post ipsum dolor"),
            (other_post, "Post ipsum dolor"),
            (recent_post, "Post ipsum dolor"),
        ]
    )

    user_permissions = user_permissions_factory(user)

    results = search.search_private_threads(
        parse_search_query("ipsum"),
        user_permissions,
        after=timezone.now() - timedelta(minutes=15),
        before=timezone.now() - timedelta(minutes=5),
        mode=search_mode,
    )

    assert len(results.items) == 1
    assert results.items[0].post_id == other_post.id
    assert results.items[0].thread_title == "Title <strong>ipsum</strong> dolor"
    assert results.items[0].post_content == "Post <strong>ipsum</strong> dolor"


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
    # We are using a mock because in default search backend this is noop
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
