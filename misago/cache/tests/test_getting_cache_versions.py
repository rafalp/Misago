from misago.cache.versions import (
    CACHE_NAME, get_cache_versions, get_cache_versions_from_cache,
    get_cache_versions_from_db
)


def test_db_getter_returns_cache_versions_from_db(db, django_assert_num_queries):
    with django_assert_num_queries(1):
        assert get_cache_versions_from_db()


def test_cache_getter_returns_cache_versions_from_cache(mocker):
    cache_get = mocker.patch('django.core.cache.cache.get', return_value=True)
    assert get_cache_versions_from_cache() is True
    cache_get.assert_called_once_with(CACHE_NAME)


def test_getter_reads_from_cache(mocker, django_assert_num_queries):
    cache_get = mocker.patch('django.core.cache.cache.get', return_value=True)
    with django_assert_num_queries(0):
        assert get_cache_versions() is True
    cache_get.assert_called_once_with(CACHE_NAME)


def test_getter_reads_from_db_if_no_cache_is_set(
    db, mocker, django_assert_num_queries
):
    mocker.patch('django.core.cache.cache.set')
    cache_get = mocker.patch('django.core.cache.cache.get', return_value=None)

    db_caches = get_cache_versions_from_db()
    with django_assert_num_queries(1):
        assert get_cache_versions() == db_caches
    cache_get.assert_called_once_with(CACHE_NAME)


def test_getter_sets_new_cache_if_no_cache_is_set(db, mocker):
    cache_set = mocker.patch('django.core.cache.cache.set')
    mocker.patch('django.core.cache.cache.get', return_value=None)

    get_cache_versions()
    db_caches = get_cache_versions_from_db()
    cache_set.assert_called_once_with(CACHE_NAME, db_caches)


def test_getter_is_not_setting_new_cache_if_cache_is_set(mocker):
    cache_set = mocker.patch('django.core.cache.cache.set')
    mocker.patch('django.core.cache.cache.get', return_value=True)
    get_cache_versions()
    cache_set.assert_not_called()