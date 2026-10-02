from ...testutils import grant_category_group_permissions
from ..enums import CategoryPermission, ThreadPostsQuery
from ..models import Moderator
from ..threads import get_threads_posts_queries


def test_get_threads_posts_queries_returns_all_posts_for_global_moderator(
    user_permissions_factory, moderator, default_category
):
    permissions = user_permissions_factory(moderator)
    queries = get_threads_posts_queries(permissions, [default_category])

    assert queries == {
        ThreadPostsQuery.ALL: {default_category.id},
    }


def test_get_threads_posts_queries_returns_all_posts_for_category_moderator(
    user_permissions_factory, user, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    permissions = user_permissions_factory(user)
    queries = get_threads_posts_queries(permissions, [default_category])

    assert queries == {
        ThreadPostsQuery.ALL: {default_category.id},
    }


def test_get_threads_posts_queries_returns_user_visible_posts_for_user(
    user_permissions_factory, user, default_category
):
    permissions = user_permissions_factory(user)
    queries = get_threads_posts_queries(permissions, [default_category])

    assert queries == {
        ThreadPostsQuery.USER: {default_category.id},
    }


def test_get_threads_posts_queries_returns_guest_visible_posts_for_anonymous_user(
    user_permissions_factory, anonymous_user, default_category
):
    permissions = user_permissions_factory(anonymous_user)
    queries = get_threads_posts_queries(permissions, [default_category])

    assert queries == {
        ThreadPostsQuery.ANON: {default_category.id},
    }


def test_get_threads_posts_queries_returns_no_query_for_invisible_category(
    user_permissions_factory, user, sibling_category
):
    permissions = user_permissions_factory(user)
    queries = get_threads_posts_queries(permissions, [sibling_category])

    assert not queries


def test_get_threads_posts_queries_returns_no_query_for_non_browseable_category(
    user_permissions_factory, user, sibling_category
):
    grant_category_group_permissions(
        sibling_category,
        user.group,
        CategoryPermission.SEE,
    )

    permissions = user_permissions_factory(user)
    queries = get_threads_posts_queries(permissions, [sibling_category])

    assert not queries


def test_get_threads_posts_queries_returns_no_query_for_non_browseable_category_with_delayed_check(
    user_permissions_factory, user, sibling_category
):
    sibling_category.delay_browse_check = True
    sibling_category.save()

    grant_category_group_permissions(
        sibling_category,
        user.group,
        CategoryPermission.SEE,
    )

    permissions = user_permissions_factory(user)
    queries = get_threads_posts_queries(permissions, [sibling_category])

    assert not queries
