from ...testutils import grant_category_group_permissions
from ...threads.models import Post
from ..enums import CategoryPermission
from ..models import Moderator
from ..threads import filter_threads_posts_queryset


def test_filter_threads_posts_queryset_returns_user_post_for_global_moderator(
    user_permissions_factory, moderator, default_category, user_reply
):
    permissions = user_permissions_factory(moderator)
    queryset = filter_threads_posts_queryset(permissions, [default_category])

    assert user_reply in list(queryset)


def test_filter_threads_posts_queryset_returns_hidden_user_post_for_global_moderator(
    user_permissions_factory, moderator, default_category, user_hidden_reply
):
    permissions = user_permissions_factory(moderator)
    queryset = filter_threads_posts_queryset(permissions, [default_category])

    assert user_hidden_reply in list(queryset)


def test_filter_threads_posts_queryset_returns_unapproved_user_post_for_global_moderator(
    user_permissions_factory, moderator, default_category, user_unapproved_reply
):
    permissions = user_permissions_factory(moderator)
    queryset = filter_threads_posts_queryset(permissions, [default_category])

    assert user_unapproved_reply in list(queryset)


def test_filter_threads_posts_queryset_returns_deleted_user_post_for_global_moderator(
    user_permissions_factory, moderator, default_category, reply
):
    permissions = user_permissions_factory(moderator)
    queryset = filter_threads_posts_queryset(permissions, [default_category])

    assert reply in list(queryset)


def test_filter_threads_posts_queryset_returns_hidden_deleted_user_post_for_global_moderator(
    user_permissions_factory, moderator, default_category, hidden_reply
):
    permissions = user_permissions_factory(moderator)
    queryset = filter_threads_posts_queryset(permissions, [default_category])

    assert hidden_reply in list(queryset)


def test_filter_threads_posts_queryset_returns_unapproved_deleted_user_post_for_global_moderator(
    user_permissions_factory, moderator, default_category, unapproved_reply
):
    permissions = user_permissions_factory(moderator)
    queryset = filter_threads_posts_queryset(permissions, [default_category])

    assert unapproved_reply in list(queryset)


def test_filter_threads_posts_queryset_returns_user_post_for_category_moderator(
    user_permissions_factory, user, default_category, user_reply
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    permissions = user_permissions_factory(user)
    queryset = filter_threads_posts_queryset(permissions, [default_category])

    assert user_reply in list(queryset)


def test_filter_threads_posts_queryset_returns_hidden_user_post_for_category_moderator(
    user_permissions_factory, user, default_category, user_hidden_reply
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    permissions = user_permissions_factory(user)
    queryset = filter_threads_posts_queryset(permissions, [default_category])

    assert user_hidden_reply in list(queryset)


def test_filter_threads_posts_queryset_returns_unapproved_user_post_for_category_moderator(
    user_permissions_factory, user, default_category, user_unapproved_reply
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    permissions = user_permissions_factory(user)
    queryset = filter_threads_posts_queryset(permissions, [default_category])

    assert user_unapproved_reply in list(queryset)


def test_filter_threads_posts_queryset_returns_deleted_user_post_for_category_moderator(
    user_permissions_factory, user, default_category, reply
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    permissions = user_permissions_factory(user)
    queryset = filter_threads_posts_queryset(permissions, [default_category])

    assert reply in list(queryset)


def test_filter_threads_posts_queryset_returns_hidden_deleted_user_post_for_category_moderator(
    user_permissions_factory, user, default_category, hidden_reply
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    permissions = user_permissions_factory(user)
    queryset = filter_threads_posts_queryset(permissions, [default_category])

    assert hidden_reply in list(queryset)


def test_filter_threads_posts_queryset_returns_unapproved_deleted_user_post_for_category_moderator(
    user_permissions_factory, user, default_category, unapproved_reply
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    permissions = user_permissions_factory(user)
    queryset = filter_threads_posts_queryset(permissions, [default_category])

    assert unapproved_reply in list(queryset)


def test_filter_threads_posts_queryset_returns_user_post_for_user(
    user_permissions_factory, user, default_category, user_reply
):
    permissions = user_permissions_factory(user)
    queryset = filter_threads_posts_queryset(permissions, [default_category])

    assert user_reply in list(queryset)


def test_filter_threads_posts_queryset_hides_hidden_user_post_from_user(
    user_permissions_factory, user, default_category, user_hidden_reply
):
    permissions = user_permissions_factory(user)
    queryset = filter_threads_posts_queryset(permissions, [default_category])

    assert user_hidden_reply not in list(queryset)


def test_filter_threads_posts_queryset_returns_unapproved_user_post_for_user(
    user_permissions_factory, user, default_category, user_unapproved_reply
):
    permissions = user_permissions_factory(user)
    queryset = filter_threads_posts_queryset(permissions, [default_category])

    assert user_unapproved_reply in list(queryset)


def test_filter_threads_posts_queryset_returns_other_user_post_for_user(
    user_permissions_factory, user, default_category, other_user_reply
):
    permissions = user_permissions_factory(user)
    queryset = filter_threads_posts_queryset(permissions, [default_category])

    assert other_user_reply in list(queryset)


def test_filter_threads_posts_queryset_hides_hidden_other_user_post_from_user(
    user_permissions_factory, user, default_category, other_user_hidden_reply
):
    permissions = user_permissions_factory(user)
    queryset = filter_threads_posts_queryset(permissions, [default_category])

    assert other_user_hidden_reply not in list(queryset)


def test_filter_threads_posts_queryset_returns_unapproved_other_user_post_for_user(
    user_permissions_factory, user, default_category, other_user_unapproved_reply
):
    permissions = user_permissions_factory(user)
    queryset = filter_threads_posts_queryset(permissions, [default_category])

    assert other_user_unapproved_reply not in list(queryset)


def test_filter_threads_posts_queryset_returns_deleted_user_post_for_user(
    user_permissions_factory, user, default_category, reply
):
    permissions = user_permissions_factory(user)
    queryset = filter_threads_posts_queryset(permissions, [default_category])

    assert reply in list(queryset)


def test_filter_threads_posts_queryset_hides_hidden_deleted_user_post_from_user(
    user_permissions_factory, user, default_category, hidden_reply
):
    permissions = user_permissions_factory(user)
    queryset = filter_threads_posts_queryset(permissions, [default_category])

    assert hidden_reply not in list(queryset)


def test_filter_threads_posts_queryset_hides_unapproved_deleted_user_post_from_user(
    user_permissions_factory, user, default_category, unapproved_reply
):
    permissions = user_permissions_factory(user)
    queryset = filter_threads_posts_queryset(permissions, [default_category])

    assert unapproved_reply not in list(queryset)


def test_filter_threads_posts_queryset_returns_user_post_for_anonymous_user(
    user_permissions_factory, anonymous_user, default_category, user_reply
):
    permissions = user_permissions_factory(anonymous_user)
    queryset = filter_threads_posts_queryset(permissions, [default_category])

    assert user_reply in list(queryset)


def test_filter_threads_posts_queryset_hides_hidden_user_post_from_anonymous_user(
    user_permissions_factory, anonymous_user, default_category, user_hidden_reply
):
    permissions = user_permissions_factory(anonymous_user)
    queryset = filter_threads_posts_queryset(permissions, [default_category])

    assert user_hidden_reply not in list(queryset)


def test_filter_threads_posts_queryset_returns_unapproved_user_post_for_anonymous_user(
    user_permissions_factory, anonymous_user, default_category, user_unapproved_reply
):
    permissions = user_permissions_factory(anonymous_user)
    queryset = filter_threads_posts_queryset(permissions, [default_category])

    assert user_unapproved_reply not in list(queryset)


def test_filter_threads_posts_queryset_returns_deleted_user_post_for_anonymous_user(
    user_permissions_factory, anonymous_user, default_category, reply
):
    permissions = user_permissions_factory(anonymous_user)
    queryset = filter_threads_posts_queryset(permissions, [default_category])

    assert reply in list(queryset)


def test_filter_threads_posts_queryset_hides_hidden_deleted_user_post_from_anonymous_user(
    user_permissions_factory, anonymous_user, default_category, hidden_reply
):
    permissions = user_permissions_factory(anonymous_user)
    queryset = filter_threads_posts_queryset(permissions, [default_category])

    assert hidden_reply not in list(queryset)


def test_filter_threads_posts_queryset_hides_unapproved_deleted_user_post_from_anonymous_user(
    user_permissions_factory, anonymous_user, default_category, unapproved_reply
):
    permissions = user_permissions_factory(anonymous_user)
    queryset = filter_threads_posts_queryset(permissions, [default_category])

    assert unapproved_reply not in list(queryset)


def test_filter_threads_posts_queryset_filters_existing_queryset(
    user_permissions_factory, user, default_category, post, reply, user_reply
):
    permissions = user_permissions_factory(user)
    queryset = filter_threads_posts_queryset(
        permissions, [default_category], Post.objects.filter(id__in=[reply.id])
    )

    assert list(queryset) == [reply]


def test_filter_threads_posts_queryset_excludes_invisible_categories(
    thread_factory, user_permissions_factory, user, sibling_category
):
    thread_factory(sibling_category)

    permissions = user_permissions_factory(user)
    queryset = filter_threads_posts_queryset(permissions, [sibling_category])

    assert not queryset


def test_filter_threads_posts_queryset_excludes_non_browseable_categories(
    thread_factory, user_permissions_factory, user, sibling_category
):
    thread_factory(sibling_category)

    grant_category_group_permissions(
        sibling_category,
        user.group,
        CategoryPermission.SEE,
    )

    permissions = user_permissions_factory(user)
    queryset = filter_threads_posts_queryset(permissions, [sibling_category])

    assert not queryset


def test_filter_threads_posts_queryset_excludes_non_browseable_categories_with_delayed_check(
    thread_factory, user_permissions_factory, user, sibling_category
):
    sibling_category.delay_browse_check = True
    sibling_category.save()

    thread_factory(sibling_category)

    grant_category_group_permissions(
        sibling_category,
        user.group,
        CategoryPermission.SEE,
    )

    permissions = user_permissions_factory(user)
    queryset = filter_threads_posts_queryset(permissions, [sibling_category])

    assert not queryset
