from ..models import Moderator
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


def test_user_permissions_proxy_returns_member_global_moderator_permission(
    django_assert_num_queries, user, cache_versions
):
    Moderator.objects.create(is_global=True, user=user)

    with django_assert_num_queries(1):
        proxy = UserPermissionsProxy(user, cache_versions)
        assert proxy.is_global_moderator


def test_user_permissions_proxy_returns_member_global_moderator_no_permission(
    django_assert_num_queries, user, cache_versions
):
    with django_assert_num_queries(1):
        proxy = UserPermissionsProxy(user, cache_versions)
        assert not proxy.is_global_moderator
