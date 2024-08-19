from ..models import Moderator
from ..proxy import UserPermissionsProxy
from ..threads import filter_thread_posts_queryset


def test_filter_thread_posts_queryset_shows_reply_to_anonymous_user(
    cache_versions, anonymous_user, thread, post, reply
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    queryset = filter_thread_posts_queryset(
        permissions, thread, thread.post_set.order_by("id")
    )

    assert post in queryset
    assert reply in queryset


def test_filter_thread_posts_queryset_shows_reply_to_user(
    cache_versions, user, thread, post, reply
):
    permissions = UserPermissionsProxy(user, cache_versions)
    queryset = filter_thread_posts_queryset(
        permissions, thread, thread.post_set.order_by("id")
    )

    assert post in queryset
    assert reply in queryset


def test_filter_thread_posts_queryset_shows_users_reply_to_anonymous_user(
    cache_versions, anonymous_user, thread, post, user_reply
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    queryset = filter_thread_posts_queryset(
        permissions, thread, thread.post_set.order_by("id")
    )

    assert post in queryset
    assert user_reply in queryset


def test_filter_thread_posts_queryset_shows_users_own_reply_to_user(
    cache_versions, user, thread, post, user_reply
):
    permissions = UserPermissionsProxy(user, cache_versions)
    queryset = filter_thread_posts_queryset(
        permissions, thread, thread.post_set.order_by("id")
    )

    assert post in queryset
    assert user_reply in queryset


def test_filter_thread_posts_queryset_shows_other_users_reply_to_user(
    cache_versions, user, thread, post, other_user_reply
):
    permissions = UserPermissionsProxy(user, cache_versions)
    queryset = filter_thread_posts_queryset(
        permissions, thread, thread.post_set.order_by("id")
    )

    assert post in queryset
    assert other_user_reply in queryset


def test_filter_thread_posts_queryset_shows_hidden_post_to_anonymous_user(
    cache_versions, anonymous_user, thread, post, hidden_reply
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    queryset = filter_thread_posts_queryset(
        permissions, thread, thread.post_set.order_by("id")
    )

    assert post in queryset
    assert hidden_reply in queryset


def test_filter_thread_posts_queryset_shows_users_hidden_post_to_anonymous_user(
    cache_versions, anonymous_user, thread, post, user_hidden_reply
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    queryset = filter_thread_posts_queryset(
        permissions, thread, thread.post_set.order_by("id")
    )

    assert post in queryset
    assert user_hidden_reply in queryset


def test_filter_thread_posts_queryset_shows_hidden_post_to_user(
    cache_versions, anonymous_user, thread, post, hidden_reply
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    queryset = filter_thread_posts_queryset(
        permissions, thread, thread.post_set.order_by("id")
    )

    assert post in queryset
    assert hidden_reply in queryset


def test_filter_thread_posts_queryset_shows_users_own_hidden_post_to_user(
    cache_versions, anonymous_user, thread, post, user_hidden_reply
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    queryset = filter_thread_posts_queryset(
        permissions, thread, thread.post_set.order_by("id")
    )

    assert post in queryset
    assert user_hidden_reply in queryset


def test_filter_thread_posts_queryset_shows_other_users_hidden_post_to_user(
    cache_versions, anonymous_user, thread, post, other_user_hidden_reply
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    queryset = filter_thread_posts_queryset(
        permissions, thread, thread.post_set.order_by("id")
    )

    assert post in queryset
    assert other_user_hidden_reply in queryset


def test_filter_thread_posts_queryset_hides_unapproved_post_from_anonymous_user(
    cache_versions, anonymous_user, thread, post, unapproved_reply
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    queryset = filter_thread_posts_queryset(
        permissions, thread, thread.post_set.order_by("id")
    )

    assert post in queryset
    assert unapproved_reply not in queryset


def test_filter_thread_posts_queryset_hides_users_unapproved_post_from_anonymous_user(
    cache_versions, anonymous_user, thread, post, user_unapproved_reply
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    queryset = filter_thread_posts_queryset(
        permissions, thread, thread.post_set.order_by("id")
    )

    assert post in queryset
    assert user_unapproved_reply not in queryset


def test_filter_thread_posts_queryset_hides_unapproved_post_from_user(
    cache_versions, user, thread, post, unapproved_reply
):
    permissions = UserPermissionsProxy(user, cache_versions)
    queryset = filter_thread_posts_queryset(
        permissions, thread, thread.post_set.order_by("id")
    )

    assert post in queryset
    assert unapproved_reply not in queryset


def test_filter_thread_posts_queryset_hides_other_users_unapproved_post_from_user(
    cache_versions, user, thread, post, other_user_unapproved_reply
):
    permissions = UserPermissionsProxy(user, cache_versions)
    queryset = filter_thread_posts_queryset(
        permissions, thread, thread.post_set.order_by("id")
    )

    assert post in queryset
    assert other_user_unapproved_reply not in queryset


def test_filter_thread_posts_queryset_shows_users_own_unapproved_post_to_user(
    cache_versions, user, thread, post, user_unapproved_reply
):
    permissions = UserPermissionsProxy(user, cache_versions)
    queryset = filter_thread_posts_queryset(
        permissions, thread, thread.post_set.order_by("id")
    )

    assert post in queryset
    assert user_unapproved_reply in queryset


def test_filter_thread_posts_queryset_shows_unapproved_post_to_global_moderator(
    cache_versions, moderator, thread, post, unapproved_reply
):
    permissions = UserPermissionsProxy(moderator, cache_versions)
    queryset = filter_thread_posts_queryset(
        permissions, thread, thread.post_set.order_by("id")
    )

    assert post in queryset
    assert unapproved_reply in queryset


def test_filter_thread_posts_queryset_shows_users_own_unapproved_post_to_global_moderator(
    cache_versions, moderator, thread, post, unapproved_reply
):
    unapproved_reply.poster = moderator
    unapproved_reply.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    queryset = filter_thread_posts_queryset(
        permissions, thread, thread.post_set.order_by("id")
    )

    assert post in queryset
    assert unapproved_reply in queryset


def test_filter_thread_posts_queryset_shows_other_users_unapproved_post_to_global_moderator(
    cache_versions, moderator, thread, post, other_user_unapproved_reply
):
    permissions = UserPermissionsProxy(moderator, cache_versions)
    queryset = filter_thread_posts_queryset(
        permissions, thread, thread.post_set.order_by("id")
    )

    assert post in queryset
    assert other_user_unapproved_reply in queryset


def test_filter_thread_posts_queryset_shows_unapproved_post_to_category_moderator(
    cache_versions, user, thread, post, unapproved_reply
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    permissions = UserPermissionsProxy(user, cache_versions)
    queryset = filter_thread_posts_queryset(
        permissions, thread, thread.post_set.order_by("id")
    )

    assert post in queryset
    assert unapproved_reply in queryset


def test_filter_thread_posts_queryset_shows_users_own_unapproved_post_to_category_moderator(
    cache_versions, user, thread, post, user_unapproved_reply
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    permissions = UserPermissionsProxy(user, cache_versions)
    queryset = filter_thread_posts_queryset(
        permissions, thread, thread.post_set.order_by("id")
    )

    assert post in queryset
    assert user_unapproved_reply in queryset


def test_filter_thread_posts_queryset_shows_other_users_unapproved_post_to_category_moderator(
    cache_versions, user, thread, post, other_user_unapproved_reply
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    permissions = UserPermissionsProxy(user, cache_versions)
    queryset = filter_thread_posts_queryset(
        permissions, thread, thread.post_set.order_by("id")
    )

    assert post in queryset
    assert other_user_unapproved_reply in queryset
