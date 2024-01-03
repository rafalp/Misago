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
