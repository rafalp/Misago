from ..useracl import get_user_acl


def test_getter_returns_authenticated_user_acl(cache_versions, user):
    acl = get_user_acl(user, cache_versions)

    assert acl
    assert acl["user_id"] == user.id
    assert acl["is_authenticated"] is True
    assert acl["is_anonymous"] is False


def test_user_acl_includes_staff_and_superuser_false_status(cache_versions, user):
    acl = get_user_acl(user, cache_versions)

    assert acl
    assert acl["is_staff"] is False
    assert acl["is_superuser"] is False


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


def test_superuser_acl_includes_staff_and_superuser_true_status(
    cache_versions, superuser
):
    acl = get_user_acl(superuser, cache_versions)

    assert acl
    assert acl["is_staff"] is True
    assert acl["is_superuser"] is True


def test_staffuser_acl_includes_staff_and_superuser_true_status(
    cache_versions, staffuser
):
    acl = get_user_acl(staffuser, cache_versions)

    assert acl
    assert acl["is_staff"] is True
    assert acl["is_superuser"] is False


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
