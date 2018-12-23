import pytest

from ..models import CacheVersion
from ..test import assert_invalidates_cache
from ..versions import invalidate_cache


def test_assertion_fails_if_specified_cache_is_not_invaldiated(cache_version):
    with pytest.raises(AssertionError):
        with assert_invalidates_cache(cache_version.cache):
            pass


def test_assertion_passess_if_specified_cache_is_invalidated(cache_version):
    with assert_invalidates_cache(cache_version.cache):
        invalidate_cache(cache_version.cache)


def test_assertion_fails_if_other_cache_is_invalidated(cache_version):
    CacheVersion.objects.create(cache="changed_test")
    with pytest.raises(AssertionError):
        with assert_invalidates_cache(cache_version.cache):
            invalidate_cache("changed_test")
