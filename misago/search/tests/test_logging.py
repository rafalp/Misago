from datetime import timedelta

from ..logging import delete_all_search_logs, delete_old_search_logs, log_search
from ..models import SearchLog


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


def test_delete_all_search_logs_deletes_all_logs(user):
    log_search(user, "127.0.0.1", "example search", is_public=True)
    log_search(None, "127.0.0.1", "example search")
    log_search(user, "127.0.0.1", "example search", is_public=True)
    log_search(None, "127.0.0.1", "example search")

    assert delete_all_search_logs() == 4
    assert not SearchLog.objects.exists()


def test_delete_old_search_logs_deletes_old_logs(user):
    log_search(user, "127.0.0.1", "example search", is_public=True)
    log_search(None, "127.0.0.1", "example search")
    log_search(user, "127.0.0.1", "example search", is_public=True)
    log_search(None, "127.0.0.1", "example search")

    for i, log in enumerate(SearchLog.objects.all()):
        log.searched_at -= timedelta(days=30 + i)
        log.save()

    assert delete_old_search_logs(20) == 4
    assert not SearchLog.objects.exists()


def test_delete_old_search_logs_deletes_old_logs(user):
    log_search(user, "127.0.0.1", "example search", is_public=True)
    log_search(None, "127.0.0.1", "example search")
    log_search(user, "127.0.0.1", "example search", is_public=True)
    log_search(None, "127.0.0.1", "example search")

    for i, log in enumerate(SearchLog.objects.all()):
        log.searched_at -= timedelta(days=30 + i)
        log.save()

    assert delete_old_search_logs(20) == 4
    assert not SearchLog.objects.exists()


def test_delete_old_search_logs_keeps_recent_logs(user):
    log_search(user, "127.0.0.1", "example search", is_public=True)
    log_search(None, "127.0.0.1", "example search")
    log_search(user, "127.0.0.1", "example search", is_public=True)
    log_search(None, "127.0.0.1", "example search")

    assert delete_old_search_logs(1) == 0
    assert SearchLog.objects.count() == 4
