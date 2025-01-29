from ...permissions.proxy import UserPermissionsProxy
from ..prefetch import prefetch_posts_related_objects


def test_prefetch_posts_related_objects_preloads_categories(
    dynamic_settings,
    cache_versions,
    anonymous_user,
    default_category,
    sibling_category,
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    data = prefetch_posts_related_objects(
        dynamic_settings,
        permissions,
        [],
        categories=[default_category, sibling_category],
    )
    assert data["categories"] == {
        default_category.id: default_category,
        sibling_category.id: sibling_category,
    }


def test_prefetch_posts_related_objects_preloads_threads(
    dynamic_settings,
    cache_versions,
    anonymous_user,
    thread,
    user_thread,
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    data = prefetch_posts_related_objects(
        dynamic_settings, permissions, [], threads=[thread, user_thread]
    )
    assert data["threads"] == {
        thread.id: thread,
        user_thread.id: user_thread,
    }


def test_prefetch_posts_related_objects_preloads_posts(
    dynamic_settings,
    cache_versions,
    anonymous_user,
    post,
    user_reply,
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    data = prefetch_posts_related_objects(
        dynamic_settings, permissions, [post, user_reply]
    )
    assert data["posts"] == {
        post.id: post,
        user_reply.id: user_reply,
    }


def test_prefetch_posts_related_objects_preloads_attachments(
    dynamic_settings,
    cache_versions,
    anonymous_user,
    attachment,
    user_attachment,
    post,
):
    attachment.category = post.category
    attachment.thread = post.thread
    attachment.post = post
    attachment.save()

    user_attachment.category = post.category
    user_attachment.thread = post.thread
    user_attachment.post = post
    user_attachment.save()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    data = prefetch_posts_related_objects(
        dynamic_settings, permissions, [], attachments=[attachment, user_attachment]
    )
    assert data["attachments"] == {
        attachment.id: attachment,
        user_attachment.id: user_attachment,
    }


def test_prefetch_posts_related_objects_removes_preloaded_attachments_without_permission(
    dynamic_settings,
    cache_versions,
    user,
    attachment,
    user_attachment,
):
    permissions = UserPermissionsProxy(user, cache_versions)

    data = prefetch_posts_related_objects(
        dynamic_settings, permissions, [], attachments=[attachment, user_attachment]
    )
    assert data["attachments"] == {
        user_attachment.id: user_attachment,
    }


def test_prefetch_posts_related_objects_preloads_users(
    dynamic_settings,
    cache_versions,
    anonymous_user,
    user,
    other_user,
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    data = prefetch_posts_related_objects(
        dynamic_settings, permissions, [], users=[user, other_user]
    )
    assert data["users"] == {
        user.id: user,
        other_user.id: other_user,
    }


def test_prefetch_posts_related_objects_prefetches_post_user(
    dynamic_settings, cache_versions, user, user_reply, django_assert_num_queries
):
    permissions = UserPermissionsProxy(user, cache_versions)

    data = prefetch_posts_related_objects(dynamic_settings, permissions, [user_reply])
    assert data["users"] == {user.id: user}

    with django_assert_num_queries(0):
        data["users"][user.id].group


def test_prefetch_posts_related_objects_prefetches_posts_users(
    dynamic_settings,
    cache_versions,
    user,
    other_user,
    user_reply,
    other_user_reply,
    django_assert_num_queries,
):
    permissions = UserPermissionsProxy(user, cache_versions)

    data = prefetch_posts_related_objects(
        dynamic_settings, permissions, [user_reply, other_user_reply]
    )
    assert data["users"] == {user.id: user, other_user.id: other_user}

    with django_assert_num_queries(0):
        assert data["users"][user.id].group
        assert data["users"][other_user.id].group


def test_prefetch_posts_related_objects_doesnt_prefetch_anonymous_posts_users(
    dynamic_settings,
    cache_versions,
    user,
    post,
    django_assert_num_queries,
):
    permissions = UserPermissionsProxy(user, cache_versions)

    data = prefetch_posts_related_objects(dynamic_settings, permissions, [post])
    assert data["users"] == {user.id: user}

    with django_assert_num_queries(0):
        assert data["users"][user.id].group


def test_prefetch_posts_related_objects_preloads_user_from_permissions(
    dynamic_settings,
    cache_versions,
    user,
    django_assert_num_queries,
):
    permissions = UserPermissionsProxy(user, cache_versions)

    data = prefetch_posts_related_objects(dynamic_settings, permissions, [])
    assert data["users"] == {user.id: user}

    with django_assert_num_queries(0):
        assert data["users"][user.id].group


def test_prefetch_posts_related_objects_doesnt_preload_anonymous_user_from_permissions(
    dynamic_settings,
    cache_versions,
    anonymous_user,
    post,
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    data = prefetch_posts_related_objects(dynamic_settings, permissions, [post])
    assert data["users"] == {}
