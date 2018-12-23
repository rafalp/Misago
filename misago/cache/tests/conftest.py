import pytest

from ..models import CacheVersion


@pytest.fixture
def cache_version(db):
    return CacheVersion.objects.create(cache="test_cache")
