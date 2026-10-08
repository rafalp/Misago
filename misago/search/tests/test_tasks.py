from datetime import timedelta

from ..logging import log_search
from ..models import SearchLog
from ..tasks import clear_old_search_logs


def test_clear_old_search_logs_clears_old_search_logs(user):
    log_search(user, "127.0.0.1", "example search", is_public=True)
    log_search(None, "127.0.0.1", "example search")
    log_search(user, "127.0.0.1", "example search", is_public=True)
    log_search(None, "127.0.0.1", "example search")

    for i, log in enumerate(SearchLog.objects.all()):
        log.searched_at -= timedelta(days=50 + i)
        log.save()

    clear_old_search_logs()

    assert not SearchLog.objects.exists()


def test_clear_old_search_logs_keeps_recent_search_logs(user):
    log_search(user, "127.0.0.1", "example search", is_public=True)
    log_search(None, "127.0.0.1", "example search")
    log_search(user, "127.0.0.1", "example search", is_public=True)
    log_search(None, "127.0.0.1", "example search")

    clear_old_search_logs()

    assert SearchLog.objects.count() == 4
