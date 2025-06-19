from ..generic import filter_accessible_thread_posts
from ..proxy import UserPermissionsProxy


def test_filter_accessible_thread_posts_filters_thread_posts_queryset(
    user, cache_versions, default_category, thread, reply, unapproved_reply
):
    permissions = UserPermissionsProxy(user, cache_versions)
    queryset = filter_accessible_thread_posts(
        permissions, default_category, thread, thread.post_set.order_by("id")
    )
    assert reply in list(queryset)
    assert unapproved_reply not in list(queryset)


def test_filter_accessible_thread_posts_filters_private_thread_posts_queryset(
    user, cache_versions, private_threads_category, private_thread
):
    permissions = UserPermissionsProxy(user, cache_versions)
    queryset = filter_accessible_thread_posts(
        permissions,
        private_threads_category,
        private_thread,
        private_thread.post_set.order_by("id"),
    )
    assert private_thread.first_post in list(queryset)
