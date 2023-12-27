from ..useracl import get_user_acl


def test_getter_returns_authenticated_user_acl(cache_versions, user):
    acl = get_user_acl(user, cache_versions)

    assert acl
    assert acl["user_id"] == user.id
    assert acl["is_authenticated"] is True
    assert acl["is_anonymous"] is False


def test_user_acl_excludes_admin_and_root_status(cache_versions, user):
    acl = get_user_acl(user, cache_versions)

    assert acl
    assert acl["is_admin"] is False
    assert acl["is_root"] is False


def test_user_acl_includes_cache_versions(cache_versions, user):
    acl = get_user_acl(user, cache_versions)

    assert acl
    assert acl["cache_versions"] == cache_versions


def test_getter_returns_anonymous_user_acl(db, cache_versions, anonymous_user):
    acl = get_user_acl(anonymous_user, cache_versions)

    assert acl
    assert acl["user_id"] == anonymous_user.id
    assert acl["is_authenticated"] is False
    assert acl["is_anonymous"] is True


def test_admin_acl_includes_admin_but_not_root_status(cache_versions, admin):
    acl = get_user_acl(admin, cache_versions)

    assert acl
    assert acl["is_admin"] is True
    assert acl["is_root"] is False


def test_root_admin_acl_includes_admin_and_root_true_status(cache_versions, root_admin):
    acl = get_user_acl(root_admin, cache_versions)

    assert acl
    assert acl["is_admin"] is True
    assert acl["is_root"] is True


def test_getter_returns_acl_from_cache(mocker, db, cache_versions, anonymous_user):
    cache_get = mocker.patch("django.core.cache.cache.get", return_value=dict())
    get_user_acl(anonymous_user, cache_versions)
    cache_get.assert_called_once()


def test_getter_builds_new_acl_when_cache_is_not_available(
    mocker, cache_versions, user
):
    mocker.patch("django.core.cache.cache.set")
    mocker.patch("misago.acl.buildacl.build_acl", return_value=dict())
    cache_get = mocker.patch("django.core.cache.cache.get", return_value=None)

    get_user_acl(user, cache_versions)
    cache_get.assert_called_once()


def test_getter_sets_new_cache_if_no_cache_is_set(
    mocker, db, cache_versions, anonymous_user
):
    cache_set = mocker.patch("django.core.cache.cache.set")
    mocker.patch("misago.acl.buildacl.build_acl", return_value=dict())
    mocker.patch("django.core.cache.cache.get", return_value=None)

    get_user_acl(anonymous_user, cache_versions)
    cache_set.assert_called_once()


def test_acl_cache_name_includes_cache_version(
    mocker, db, cache_versions, anonymous_user
):
    cache_set = mocker.patch("django.core.cache.cache.set")
    mocker.patch("misago.acl.buildacl.build_acl", return_value=dict())
    mocker.patch("django.core.cache.cache.get", return_value=None)

    get_user_acl(anonymous_user, cache_versions)
    cache_key = cache_set.call_args[0][0]
    assert cache_versions["acl"] in cache_key


def test_getter_is_not_setting_new_cache_if_cache_is_set(
    mocker, cache_versions, anonymous_user
):
    cache_set = mocker.patch("django.core.cache.cache.set")
    mocker.patch("django.core.cache.cache.get", return_value=dict())

    get_user_acl(anonymous_user, cache_versions)
    cache_set.assert_not_called()
