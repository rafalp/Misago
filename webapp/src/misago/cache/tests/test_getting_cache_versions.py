from ..versions import get_cache_versions


def test_getter_returns_cache_versions(db):
    assert get_cache_versions()
