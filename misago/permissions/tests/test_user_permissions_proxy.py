from ..enums import CategoryPermission
from ..models import CategoryGroupPermission, Moderator
from ..proxy import UserPermissionsProxy


def test_user_permissions_proxy_makes_no_queries_unused(
    django_assert_num_queries, user, cache_versions
):
    with django_assert_num_queries(0):
        proxy = UserPermissionsProxy(user, cache_versions)
        assert not proxy.accessed_permissions


def test_user_permissions_proxy_returns_user_permissions(user, cache_versions):
    proxy = UserPermissionsProxy(user, cache_versions)
    permissions = proxy.permissions
    assert permissions["categories"]
    assert proxy.accessed_permissions


def test_user_permissions_proxy_getattr_returns_user_permission(user, cache_versions):
    proxy = UserPermissionsProxy(user, cache_versions)
    assert proxy.categories
    assert proxy.accessed_permissions


def test_user_permissions_proxy_returns_admins_member_global_moderator_permission(
    django_assert_num_queries, user, admins_group, cache_versions
):
    user.set_groups(admins_group)
    user.save()

    with django_assert_num_queries(0):
        proxy = UserPermissionsProxy(user, cache_versions)
        assert proxy.is_global_moderator


def test_user_permissions_proxy_returns_moderators_member_global_moderator_permission(
    django_assert_num_queries, user, moderators_group, cache_versions
):
    user.set_groups(moderators_group)
    user.save()

    with django_assert_num_queries(0):
        proxy = UserPermissionsProxy(user, cache_versions)
        assert proxy.is_global_moderator


def test_user_permissions_proxy_returns_secondary_admins_member_global_moderator_permission(
    django_assert_num_queries, user, members_group, admins_group, cache_versions
):
    user.set_groups(members_group, [admins_group])
    user.save()

    with django_assert_num_queries(0):
        proxy = UserPermissionsProxy(user, cache_versions)
        assert proxy.is_global_moderator


def test_user_permissions_proxy_returns_secondary_moderators_member_global_moderator_permission(
    django_assert_num_queries, user, members_group, moderators_group, cache_versions
):
    user.set_groups(members_group, [moderators_group])
    user.save()

    with django_assert_num_queries(0):
        proxy = UserPermissionsProxy(user, cache_versions)
        assert proxy.is_global_moderator


def test_user_permissions_proxy_returns_custom_moderators_member_global_moderator_permission(
    django_assert_num_queries, user, custom_group, cache_versions
):
    Moderator.objects.create(is_global=True, group=custom_group)

    user.set_groups(custom_group)
    user.save()

    with django_assert_num_queries(1):
        proxy = UserPermissionsProxy(user, cache_versions)
        assert proxy.is_global_moderator


def test_user_permissions_proxy_returns_custom_moderators_secondary_member_global_moderator_permission(
    django_assert_num_queries, user, members_group, custom_group, cache_versions
):
    Moderator.objects.create(is_global=True, group=custom_group)

    user.set_groups(members_group, [custom_group])
    user.save()

    with django_assert_num_queries(1):
        proxy = UserPermissionsProxy(user, cache_versions)
        assert proxy.is_global_moderator


def test_user_permissions_proxy_returns_true_for_member_global_moderator_permission(
    django_assert_num_queries, user, cache_versions
):
    Moderator.objects.create(is_global=True, user=user)

    with django_assert_num_queries(1):
        proxy = UserPermissionsProxy(user, cache_versions)
        assert proxy.is_global_moderator


def test_user_permissions_proxy_returns_false_for_member_without_global_moderator_permission(
    django_assert_num_queries, user, cache_versions
):
    with django_assert_num_queries(1):
        proxy = UserPermissionsProxy(user, cache_versions)
        assert not proxy.is_global_moderator


def test_user_permissions_proxy_returns_false_for_member_without_global_moderator_permission(
    django_assert_num_queries, user, cache_versions
):
    with django_assert_num_queries(1):
        proxy = UserPermissionsProxy(user, cache_versions)
        assert not proxy.is_global_moderator


def test_user_permissions_proxy_returns_admins_member_private_threads_moderator_permission(
    django_assert_num_queries, user, admins_group, cache_versions
):
    user.set_groups(admins_group)
    user.save()

    with django_assert_num_queries(0):
        proxy = UserPermissionsProxy(user, cache_versions)
        assert proxy.is_private_threads_moderator


def test_user_permissions_proxy_returns_moderators_member_private_threads_moderator_permission(
    django_assert_num_queries, user, moderators_group, cache_versions
):
    user.set_groups(moderators_group)
    user.save()

    with django_assert_num_queries(0):
        proxy = UserPermissionsProxy(user, cache_versions)
        assert proxy.is_private_threads_moderator


def test_user_permissions_proxy_returns_secondary_admins_member_private_threads_moderator_permission(
    django_assert_num_queries, user, members_group, admins_group, cache_versions
):
    user.set_groups(members_group, [admins_group])
    user.save()

    with django_assert_num_queries(0):
        proxy = UserPermissionsProxy(user, cache_versions)
        assert proxy.is_private_threads_moderator


def test_user_permissions_proxy_returns_secondary_moderators_member_private_threads_moderator_permission(
    django_assert_num_queries, user, members_group, moderators_group, cache_versions
):
    user.set_groups(members_group, [moderators_group])
    user.save()

    with django_assert_num_queries(0):
        proxy = UserPermissionsProxy(user, cache_versions)
        assert proxy.is_private_threads_moderator


def test_user_permissions_proxy_returns_custom_moderators_member_private_threads_moderator_permission(
    django_assert_num_queries, user, custom_group, cache_versions
):
    Moderator.objects.create(is_global=False, private_threads=True, group=custom_group)

    user.set_groups(custom_group)
    user.save()

    with django_assert_num_queries(1):
        proxy = UserPermissionsProxy(user, cache_versions)
        assert proxy.is_private_threads_moderator


def test_user_permissions_proxy_returns_custom_moderators_secondary_member_private_threads_moderator_permission(
    django_assert_num_queries, user, members_group, custom_group, cache_versions
):
    Moderator.objects.create(is_global=False, private_threads=True, group=custom_group)

    user.set_groups(members_group, [custom_group])
    user.save()

    with django_assert_num_queries(1):
        proxy = UserPermissionsProxy(user, cache_versions)
        assert proxy.is_private_threads_moderator


def test_user_permissions_proxy_returns_true_for_member_private_threads_moderator_permission(
    django_assert_num_queries, user, cache_versions
):
    Moderator.objects.create(is_global=False, private_threads=True, user=user)

    with django_assert_num_queries(1):
        proxy = UserPermissionsProxy(user, cache_versions)
        assert proxy.is_private_threads_moderator


def test_user_permissions_proxy_returns_false_for_member_without_private_threads_moderator_permission(
    django_assert_num_queries, user, cache_versions
):
    with django_assert_num_queries(1):
        proxy = UserPermissionsProxy(user, cache_versions)
        assert not proxy.is_private_threads_moderator


def test_user_permissions_proxy_returns_false_for_member_without_private_threads_moderator_permission(
    django_assert_num_queries, user, cache_versions
):
    with django_assert_num_queries(1):
        proxy = UserPermissionsProxy(user, cache_versions)
        assert not proxy.is_private_threads_moderator


def test_user_permissions_proxy_returns_false_for_category_moderator(
    django_assert_num_queries, user, cache_versions, other_category
):
    Moderator.objects.create(is_global=False, user=user, categories=[other_category.id])

    with django_assert_num_queries(1):
        proxy = UserPermissionsProxy(user, cache_versions)
        assert not proxy.is_global_moderator


def test_user_permissions_proxy_returns_list_of_moderated_categories_ids_for_global_moderator(
    django_assert_num_queries,
    user,
    moderators_group,
    cache_versions,
    default_category,
    other_category,
):
    CategoryGroupPermission.objects.create(
        category=other_category,
        group=moderators_group,
        permission=CategoryPermission.SEE,
    )
    CategoryGroupPermission.objects.create(
        category=other_category,
        group=moderators_group,
        permission=CategoryPermission.BROWSE,
    )

    user.set_groups(moderators_group)
    user.save()

    proxy = UserPermissionsProxy(user, cache_versions)
    proxy.permissions

    with django_assert_num_queries(0):
        assert proxy.moderated_categories == {default_category.id, other_category.id}


def test_user_permissions_proxy_returns_list_of_moderated_categories_ids_for_local_moderator(
    django_assert_num_queries, user, cache_versions, other_category
):
    CategoryGroupPermission.objects.create(
        category=other_category,
        group=user.group,
        permission=CategoryPermission.SEE,
    )
    CategoryGroupPermission.objects.create(
        category=other_category,
        group=user.group,
        permission=CategoryPermission.BROWSE,
    )

    Moderator.objects.create(is_global=False, user=user, categories=[other_category.id])

    proxy = UserPermissionsProxy(user, cache_versions)
    proxy.permissions

    with django_assert_num_queries(1):
        assert proxy.moderated_categories == {other_category.id}


def test_user_permissions_proxy_excludes_not_browseable_categories_from_moderated_categories(
    django_assert_num_queries, user, cache_versions, other_category
):
    CategoryGroupPermission.objects.create(
        category=other_category,
        group=user.group,
        permission=CategoryPermission.SEE,
    )

    Moderator.objects.create(is_global=False, user=user, categories=[other_category.id])

    proxy = UserPermissionsProxy(user, cache_versions)
    proxy.permissions

    with django_assert_num_queries(1):
        assert proxy.moderated_categories == set()


def test_user_permissions_is_category_moderator_returns_true_for_global_moderator(
    user,
    moderators_group,
    cache_versions,
    default_category,
    other_category,
):
    CategoryGroupPermission.objects.create(
        category=other_category,
        group=moderators_group,
        permission=CategoryPermission.SEE,
    )
    CategoryGroupPermission.objects.create(
        category=other_category,
        group=moderators_group,
        permission=CategoryPermission.BROWSE,
    )

    user.set_groups(moderators_group)
    user.save()

    proxy = UserPermissionsProxy(user, cache_versions)
    proxy.permissions

    assert proxy.is_category_moderator(default_category.id)
    assert proxy.is_category_moderator(other_category.id)


def test_user_permissions_is_category_moderator_returns_true_for_category_moderator(
    user,
    cache_versions,
    default_category,
    other_category,
):
    CategoryGroupPermission.objects.create(
        category=other_category,
        group=user.group,
        permission=CategoryPermission.SEE,
    )
    CategoryGroupPermission.objects.create(
        category=other_category,
        group=user.group,
        permission=CategoryPermission.BROWSE,
    )

    proxy = UserPermissionsProxy(user, cache_versions)
    proxy.permissions

    Moderator.objects.create(is_global=False, user=user, categories=[other_category.id])

    assert not proxy.is_category_moderator(default_category.id)
    assert proxy.is_category_moderator(other_category.id)


def test_user_permissions_is_category_moderator_returns_true_for_category_moderator(
    user,
    cache_versions,
    default_category,
    other_category,
):
    CategoryGroupPermission.objects.create(
        category=other_category,
        group=user.group,
        permission=CategoryPermission.SEE,
    )
    CategoryGroupPermission.objects.create(
        category=other_category,
        group=user.group,
        permission=CategoryPermission.BROWSE,
    )

    proxy = UserPermissionsProxy(user, cache_versions)
    proxy.permissions

    Moderator.objects.create(is_global=False, user=user, categories=[other_category.id])

    assert not proxy.is_category_moderator(default_category.id)
    assert proxy.is_category_moderator(other_category.id)


def test_user_permissions_proxy_returns_false_global_moderator_for_anonymous_user(
    django_assert_num_queries, db, anonymous_user, cache_versions
):
    proxy = UserPermissionsProxy(anonymous_user, cache_versions)

    with django_assert_num_queries(0):
        assert not proxy.is_global_moderator


def test_user_permissions_proxy_returns_false_private_threads_moderator_for_anonymous_user(
    django_assert_num_queries, db, anonymous_user, cache_versions
):
    proxy = UserPermissionsProxy(anonymous_user, cache_versions)

    with django_assert_num_queries(0):
        assert not proxy.is_private_threads_moderator


def test_user_permissions_proxy_returns_no_moderated_categories_for_anonymous_user(
    django_assert_num_queries, db, anonymous_user, cache_versions
):
    proxy = UserPermissionsProxy(anonymous_user, cache_versions)
    proxy.permissions

    with django_assert_num_queries(0):
        assert not proxy.moderated_categories


def test_user_permissions_proxy_is_category_moderator_returns_false_for_anonymous_user(
    django_assert_num_queries, anonymous_user, cache_versions, default_category
):
    proxy = UserPermissionsProxy(anonymous_user, cache_versions)
    proxy.permissions

    with django_assert_num_queries(0):
        assert not proxy.is_category_moderator(default_category.id)
