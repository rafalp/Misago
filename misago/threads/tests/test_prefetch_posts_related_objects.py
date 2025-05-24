from ...conf.test import override_dynamic_settings
from ...permissions.proxy import UserPermissionsProxy
from ..prefetch import prefetch_posts_related_objects


def test_prefetch_posts_related_objects_preloads_categories(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    anonymous_user,
    default_category,
    sibling_category,
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    with django_assert_num_queries(0):
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


def test_prefetch_posts_related_objects_prefetches_threads_categories(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    anonymous_user,
    default_category,
    thread,
    user_thread,
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    with django_assert_num_queries(1):
        data = prefetch_posts_related_objects(
            dynamic_settings, permissions, [], threads=[thread, user_thread]
        )
        assert data["categories"] == {default_category.id: default_category}


def test_prefetch_posts_related_objects_prefetches_posts_categories(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    anonymous_user,
    default_category,
    post,
    user_reply,
    other_user_reply,
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    with django_assert_num_queries(5):
        data = prefetch_posts_related_objects(
            dynamic_settings, permissions, [post, user_reply, other_user_reply]
        )
        assert data["categories"] == {default_category.id: default_category}


def test_prefetch_posts_related_objects_prefetches_attachments_categories(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    anonymous_user,
    default_category,
    text_attachment,
    user_text_attachment,
    post,
):
    text_attachment.associate_with_post(post)
    text_attachment.save()

    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    with django_assert_num_queries(3):
        data = prefetch_posts_related_objects(
            dynamic_settings,
            permissions,
            [],
            attachments=[text_attachment, user_text_attachment],
        )
        assert data["categories"] == {default_category.id: default_category}


def test_prefetch_posts_related_objects_preloads_threads(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    anonymous_user,
    thread,
    user_thread,
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    with django_assert_num_queries(1):
        data = prefetch_posts_related_objects(
            dynamic_settings, permissions, [], threads=[thread, user_thread]
        )
        assert data["threads"] == {
            thread.id: thread,
            user_thread.id: user_thread,
        }


def test_prefetch_posts_related_objects_prefetches_posts_threads(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    anonymous_user,
    thread,
    post,
    user_reply,
    other_user_reply,
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    with django_assert_num_queries(5):
        data = prefetch_posts_related_objects(
            dynamic_settings, permissions, [post, user_reply, other_user_reply]
        )
        assert data["threads"] == {thread.id: thread}


def test_prefetch_posts_related_objects_prefetches_attachments_threads(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    anonymous_user,
    thread,
    post,
    text_attachment,
):
    text_attachment.associate_with_post(post)
    text_attachment.save()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    with django_assert_num_queries(3):
        data = prefetch_posts_related_objects(
            dynamic_settings, permissions, [], attachments=[text_attachment]
        )
        assert data["threads"] == {thread.id: thread}


def test_prefetch_posts_related_objects_prefetches_private_threads_members(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    anonymous_user,
    user_private_thread,
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    with django_assert_num_queries(2):
        prefetch_posts_related_objects(
            dynamic_settings, permissions, [], threads=[user_private_thread]
        )

    with django_assert_num_queries(0):
        user_private_thread.private_thread_member_ids


def test_prefetch_posts_related_objects_preloads_posts(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    anonymous_user,
    post,
    user_reply,
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    with django_assert_num_queries(5):
        data = prefetch_posts_related_objects(
            dynamic_settings, permissions, [post, user_reply]
        )
        assert data["posts"] == {
            post.id: post,
            user_reply.id: user_reply,
        }


def test_prefetch_posts_related_objects_prefetches_quoted_posts(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    anonymous_user,
    post,
    user_reply,
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    post.metadata["posts"] = [user_reply.id]

    with django_assert_num_queries(6):
        data = prefetch_posts_related_objects(dynamic_settings, permissions, [post])
        assert data["posts"] == {
            post.id: post,
            user_reply.id: user_reply,
        }


def test_prefetch_posts_related_objects_prefetches_quoted_posts_for_unsaved_post(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    anonymous_user,
    post,
    user_reply,
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    post.id = None
    post.metadata["posts"] = [user_reply.id]

    with django_assert_num_queries(5):
        data = prefetch_posts_related_objects(dynamic_settings, permissions, [post])
        assert data["posts"] == {
            user_reply.id: user_reply,
        }


def test_prefetch_posts_related_objects_prefetches_attachments_posts(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    anonymous_user,
    post,
    user_reply,
    text_attachment,
    user_text_attachment,
):
    text_attachment.associate_with_post(post)
    text_attachment.save()

    user_text_attachment.associate_with_post(user_reply)
    user_text_attachment.save()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    with django_assert_num_queries(5):
        data = prefetch_posts_related_objects(
            dynamic_settings,
            permissions,
            [],
            attachments=[text_attachment, user_text_attachment],
        )
        assert data["posts"] == {
            post.id: post,
            user_reply.id: user_reply,
        }


def test_prefetch_posts_related_objects_preloads_attachments(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    anonymous_user,
    text_attachment,
    user_text_attachment,
    post,
):
    text_attachment.associate_with_post(post)
    text_attachment.save()

    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    with django_assert_num_queries(3):
        data = prefetch_posts_related_objects(
            dynamic_settings,
            permissions,
            [],
            attachments=[text_attachment, user_text_attachment],
        )
        assert data["attachments"] == {
            text_attachment.id: text_attachment,
            user_text_attachment.id: user_text_attachment,
        }


def test_prefetch_posts_related_objects_removes_preloaded_attachments_without_permission(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    user,
    text_attachment,
    user_text_attachment,
):
    permissions = UserPermissionsProxy(user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    with django_assert_num_queries(1):
        data = prefetch_posts_related_objects(
            dynamic_settings,
            permissions,
            [],
            attachments=[text_attachment, user_text_attachment],
        )
        assert data["attachments"] == {
            user_text_attachment.id: user_text_attachment,
        }


def test_prefetch_posts_related_objects_fetches_posts_attachments(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    anonymous_user,
    text_attachment,
    user_text_attachment,
    post,
    user_reply,
):
    text_attachment.associate_with_post(post)
    text_attachment.save()

    user_text_attachment.associate_with_post(user_reply)
    user_text_attachment.save()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    with django_assert_num_queries(5):
        data = prefetch_posts_related_objects(
            dynamic_settings, permissions, [post, user_reply]
        )
        assert data["attachments"] == {
            text_attachment.id: text_attachment,
            user_text_attachment.id: user_text_attachment,
        }


def test_prefetch_posts_related_objects_fetches_posts_metadata_attachments(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    anonymous_user,
    text_attachment,
    user_text_attachment,
    post,
    user_reply,
    other_user_reply,
):
    text_attachment.associate_with_post(other_user_reply)
    text_attachment.save()

    user_text_attachment.associate_with_post(other_user_reply)
    user_text_attachment.save()

    post.metadata["attachments"] = [text_attachment.id]
    post.save()

    user_reply.metadata["attachments"] = [user_text_attachment.id]
    user_reply.save()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    with django_assert_num_queries(6):
        data = prefetch_posts_related_objects(
            dynamic_settings, permissions, [post, user_reply]
        )
        assert data["attachments"] == {
            text_attachment.id: text_attachment,
            user_text_attachment.id: user_text_attachment,
        }


@override_dynamic_settings(additional_embedded_attachments_limit=0)
def test_prefetch_posts_related_objects_doesnt_fetch_posts_metadata_attachments_if_its_disabled(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    anonymous_user,
    text_attachment,
    user_text_attachment,
    post,
    user_reply,
    other_user_reply,
):
    text_attachment.associate_with_post(other_user_reply)
    text_attachment.save()

    user_text_attachment.associate_with_post(other_user_reply)
    user_text_attachment.save()

    post.metadata["attachments"] = [text_attachment.id]
    post.save()

    user_reply.metadata["attachments"] = [user_text_attachment.id]
    user_reply.save()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    with django_assert_num_queries(5):
        data = prefetch_posts_related_objects(
            dynamic_settings, permissions, [post, user_reply]
        )
        assert data["attachments"] == {}


@override_dynamic_settings(additional_embedded_attachments_limit=1)
def test_prefetch_posts_related_objects_fetch_posts_metadata_attachments_is_limited(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    anonymous_user,
    text_attachment,
    user_text_attachment,
    post,
    user_reply,
    other_user_reply,
):
    text_attachment.associate_with_post(other_user_reply)
    text_attachment.save()

    user_text_attachment.associate_with_post(other_user_reply)
    user_text_attachment.save()

    post.metadata["attachments"] = [text_attachment.id]
    post.save()

    user_reply.metadata["attachments"] = [user_text_attachment.id]
    user_reply.save()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    with django_assert_num_queries(6):
        data = prefetch_posts_related_objects(
            dynamic_settings, permissions, [post, user_reply]
        )
        assert data["attachments"] == {user_text_attachment.id: user_text_attachment}


def test_prefetch_posts_related_objects_fetch_posts_metadata_attachments_excludes_unused_attachments(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    user,
    text_attachment,
    user_text_attachment,
    post,
    user_reply,
    other_user_reply,
):
    text_attachment.associate_with_post(other_user_reply)
    text_attachment.save()

    post.metadata["attachments"] = [text_attachment.id]
    post.save()

    user_reply.metadata["attachments"] = [user_text_attachment.id]
    user_reply.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    with django_assert_num_queries(6):
        data = prefetch_posts_related_objects(
            dynamic_settings, permissions, [post, user_reply]
        )
        assert data["attachments"] == {
            text_attachment.id: text_attachment,
        }


def test_prefetch_posts_related_objects_fetch_posts_metadata_attachments_excludes_inaccessible_attachments(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    anonymous_user,
    text_attachment,
    user_text_attachment,
    post,
    user_reply,
    other_user_reply,
    private_thread,
):
    text_attachment.associate_with_post(other_user_reply)
    text_attachment.save()

    user_text_attachment.associate_with_post(private_thread.first_post)
    user_text_attachment.save()

    post.metadata["attachments"] = [text_attachment.id]
    post.save()

    user_reply.metadata["attachments"] = [user_text_attachment.id]
    user_reply.save()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    with django_assert_num_queries(7):
        data = prefetch_posts_related_objects(
            dynamic_settings, permissions, [post, user_reply]
        )
        assert data["attachments"] == {
            text_attachment.id: text_attachment,
        }
        assert data["attachment_errors"][user_text_attachment.id].not_found


def test_prefetch_posts_related_objects_fetches_posts_metadata_posts(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    anonymous_user,
    post,
    user_reply,
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    post.metadata["posts"] = [user_reply.id]
    post.save()

    with django_assert_num_queries(6):
        data = prefetch_posts_related_objects(dynamic_settings, permissions, [post])
        assert data["posts"] == {
            post.id: post,
            user_reply.id: user_reply,
        }


def test_prefetch_posts_related_objects_preloads_users(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    anonymous_user,
    user,
    other_user,
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    with django_assert_num_queries(1):
        data = prefetch_posts_related_objects(
            dynamic_settings, permissions, [], users=[user, other_user]
        )
        assert data["users"] == {
            user.id: user,
            other_user.id: other_user,
        }


def test_prefetch_posts_related_objects_preloads_user_from_permissions(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    user,
):
    permissions = UserPermissionsProxy(user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    with django_assert_num_queries(1):
        data = prefetch_posts_related_objects(dynamic_settings, permissions, [])
        assert data["users"] == {user.id: user}

    with django_assert_num_queries(0):
        assert data["users"][user.id].group


def test_prefetch_posts_related_objects_doesnt_preload_anonymous_user_from_permissions(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    anonymous_user,
    post,
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    with django_assert_num_queries(3):
        data = prefetch_posts_related_objects(dynamic_settings, permissions, [post])
        assert data["users"] == {}


def test_prefetch_posts_related_objects_prefetches_posts_users(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    user,
    other_user,
    user_reply,
    other_user_reply,
):
    permissions = UserPermissionsProxy(user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    with django_assert_num_queries(5):
        data = prefetch_posts_related_objects(
            dynamic_settings, permissions, [user_reply, other_user_reply]
        )
        assert data["users"] == {user.id: user, other_user.id: other_user}

    with django_assert_num_queries(0):
        assert data["users"][user.id].group
        assert data["users"][other_user.id].group


def test_prefetch_posts_related_objects_doesnt_prefetch_anonymous_posts_users(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    user,
    post,
):
    permissions = UserPermissionsProxy(user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    with django_assert_num_queries(4):
        data = prefetch_posts_related_objects(dynamic_settings, permissions, [post])
        assert data["users"] == {user.id: user}

    with django_assert_num_queries(0):
        assert data["users"][user.id].group


def test_prefetch_posts_related_objects_sets_visible_posts(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    user,
    post,
    user_reply,
    hidden_reply,
    private_thread,
    user_private_thread,
):
    permissions = UserPermissionsProxy(user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    post.metadata["posts"] = [
        private_thread.first_post_id,
        user_private_thread.first_post_id,
    ]
    post.save()

    with django_assert_num_queries(6):
        data = prefetch_posts_related_objects(
            dynamic_settings, permissions, [post, user_reply, hidden_reply]
        )
        assert data["visible_posts"] == {
            post.id,
            user_reply.id,
            user_private_thread.first_post_id,
        }


def test_prefetch_posts_related_objects_prefetches_objects_in_cascade(
    django_assert_num_queries,
    dynamic_settings,
    cache_versions,
    user,
    other_user,
    default_category,
    private_threads_category,
    thread,
    post,
    user_reply,
    other_user_reply,
    user_private_thread,
    text_attachment,
    user_text_attachment,
    other_user_text_attachment,
):
    permissions = UserPermissionsProxy(user, cache_versions)
    permissions.permissions
    permissions.is_global_moderator

    text_attachment.associate_with_post(post)
    text_attachment.save()

    other_user_text_attachment.associate_with_post(user_private_thread.first_post)
    other_user_text_attachment.save()

    user_reply.metadata["attachments"] = [
        user_text_attachment.id,
        other_user_text_attachment.id,
    ]
    user_reply.save()

    with django_assert_num_queries(7):
        data = prefetch_posts_related_objects(
            dynamic_settings,
            permissions,
            [post, user_reply, other_user_reply],
        )

        assert default_category.id in data["categories"]
        assert private_threads_category.id in data["categories"]

        assert thread.id in data["threads"]
        assert user_private_thread.id in data["threads"]

        assert data["threads"][user_private_thread.id].private_thread_member_ids

        assert post.id in data["posts"]
        assert user_reply.id in data["posts"]
        assert other_user_reply.id in data["posts"]
        assert user_private_thread.first_post_id in data["posts"]

        assert user.id in data["users"]
        assert other_user.id in data["users"]

        assert data["users"][user.id].group
        assert data["users"][other_user.id].group

        assert text_attachment.id in data["attachments"]
        assert other_user_text_attachment.id in data["attachments"]
