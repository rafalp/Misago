from ..logging import log_search


def test_log_search_logs_user_public_search(user):
    search_log = log_search(user, "127.0.0.1", "example search", is_public=True)

    assert search_log.user == user
    assert search_log.ip_address == "127.0.0.1"
    assert search_log.search_query == "example search"
    assert search_log.is_public
    assert search_log.searched_at


def test_log_search_logs_user_private_search(user):
    search_log = log_search(user, "127.0.0.1", "example search")

    assert search_log.user == user
    assert search_log.ip_address == "127.0.0.1"
    assert search_log.search_query == "example search"
    assert not search_log.is_public
    assert search_log.searched_at


def test_log_search_logs_deleted_user_public_search(db):
    search_log = log_search(None, "127.0.0.1", "example search", is_public=True)

    assert search_log.user is None
    assert search_log.ip_address == "127.0.0.1"
    assert search_log.search_query == "example search"
    assert search_log.is_public
    assert search_log.searched_at


def test_log_search_logs_deleted_user_private_search(db):
    search_log = log_search(None, "127.0.0.1", "example search")

    assert search_log.user is None
    assert search_log.ip_address == "127.0.0.1"
    assert search_log.search_query == "example search"
    assert not search_log.is_public
    assert search_log.searched_at
