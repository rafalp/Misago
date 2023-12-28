import pytest
from django.core.exceptions import ObjectDoesNotExist

from ...cache.models import CacheVersion
from ..delete import delete_all, delete_one


def test_one_object_is_deleted_from_database(db):
    cache_version = CacheVersion.objects.create(cache="test", version="test")

    result = delete_one(cache_version)
    assert result == 1

    with pytest.raises(ObjectDoesNotExist):
        cache_version.refresh_from_db()


def test_one_object_is_deleted_from_database(db):
    cache_version = CacheVersion.objects.create(cache="test", version="test")

    result = delete_one(cache_version)
    assert result == 1

    with pytest.raises(ObjectDoesNotExist):
        cache_version.refresh_from_db()


def test_multiple_objects_are_deleted_from_database_using_column_equals(db):
    cache_version_1 = CacheVersion.objects.create(cache="test_1", version="test")
    cache_version_2 = CacheVersion.objects.create(cache="test_2", version="test")
    cache_version_3 = CacheVersion.objects.create(cache="test_3", version="other")

    result = delete_all(CacheVersion, version="test")
    assert result == 2

    with pytest.raises(ObjectDoesNotExist):
        cache_version_1.refresh_from_db()
    with pytest.raises(ObjectDoesNotExist):
        cache_version_2.refresh_from_db()

    cache_version_3.refresh_from_db()


def test_multiple_objects_are_deleted_from_database_using_column_in(db):
    cache_version_1 = CacheVersion.objects.create(cache="test_1", version="test")
    cache_version_2 = CacheVersion.objects.create(cache="test_2", version="test")
    cache_version_3 = CacheVersion.objects.create(cache="test_3", version="other")

    result = delete_all(CacheVersion, cache=["test_1", "test_2"])
    assert result == 2

    with pytest.raises(ObjectDoesNotExist):
        cache_version_1.refresh_from_db()
    with pytest.raises(ObjectDoesNotExist):
        cache_version_2.refresh_from_db()

    cache_version_3.refresh_from_db()


def test_multiple_objects_are_deleted_from_database_using_column_and_column(db):
    cache_version_1 = CacheVersion.objects.create(cache="test_1", version="delete")
    cache_version_2 = CacheVersion.objects.create(cache="test_2", version="test")
    cache_version_3 = CacheVersion.objects.create(cache="test_3", version="other")

    result = delete_all(CacheVersion, cache=["test_1", "test_2"], version="delete")
    assert result == 1

    with pytest.raises(ObjectDoesNotExist):
        cache_version_1.refresh_from_db()

    cache_version_2.refresh_from_db()
    cache_version_3.refresh_from_db()


def test_delete_all_raises_value_error_if_where_clause_is_not_set(db):
    cache_version_1 = CacheVersion.objects.create(cache="test_1", version="delete")
    cache_version_2 = CacheVersion.objects.create(cache="test_2", version="test")
    cache_version_3 = CacheVersion.objects.create(cache="test_3", version="other")

    with pytest.raises(ValueError):
        delete_all(CacheVersion)

    # No rows have been deleted
    cache_version_1.refresh_from_db()
    cache_version_2.refresh_from_db()
    cache_version_3.refresh_from_db()
