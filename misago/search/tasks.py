from logging import getLogger

from celery import shared_task

from ..conf.shortcuts import get_dynamic_settings
from .logging import delete_old_search_logs

logger = getLogger("misago.search")


@shared_task(name="search.clear-old-search-logs")
def clear_old_search_logs():
    settings = get_dynamic_settings()
    deleted = delete_old_search_logs(settings.search_log_retention)
    logger.info("Deleted old search logs: %s", deleted)
