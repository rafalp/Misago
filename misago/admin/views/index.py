from datetime import timedelta
from math import ceil

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.http import HttpRequest
from django.utils import timezone

from ...attachments.storage import (
    get_total_attachment_storage_usage,
    get_total_unused_attachments_size,
)
from ...threads.models import Post, Thread, Attachment
from ...users.models import DataDownload
from . import render

VERSION_CHECK_CACHE_KEY = "misago_version_check"

User = get_user_model()


def admin_index(request: HttpRequest):
    totals = count_db_items()
    checks = {
        "address": check_forum_address(request),
        "cache": check_cache(),
        "data_downloads": check_data_downloads(),
        "debug": check_debug_status(),
        "https": check_https(request),
        "attachments_storage": check_attachments_storage(request, totals),
        "inactive_users": check_inactive_users(),
    }

    return render(
        request,
        "misago/admin/dashboard/index.html",
        {"totals": totals, "checks": checks},
    )


def check_cache():
    cache.set("misago_cache_test", "ok")
    return {"is_ok": cache.get("misago_cache_test") == "ok"}


def check_debug_status():
    return {"is_ok": not settings.DEBUG}


def check_https(request: HttpRequest):
    return {"is_ok": request.is_secure()}


def check_forum_address(request: HttpRequest):
    set_address = request.settings.forum_address
    correct_address = request.build_absolute_uri("/").rstrip("/")

    return {
        "is_ok": set_address == correct_address,
        "set_address": set_address,
        "correct_address": correct_address,
    }


def check_data_downloads():
    cutoff = timezone.now() - timedelta(days=3)
    unprocessed_count = DataDownload.objects.filter(
        status__lte=DataDownload.STATUS_PROCESSING, requested_on__lte=cutoff
    ).count()

    return {"is_ok": unprocessed_count == 0, "count": unprocessed_count}


def check_attachments_storage(request: HttpRequest, totals: dict[str, int]):
    unused_limit = request.settings.unused_attachments_storage_limit * 1024 * 1024
    if not unused_limit:
        return {"is_ok": True, "limit": unused_limit}

    unused_size = totals["attachments_unused_size"]

    return {
        "is_ok": unused_size < int(unused_limit / 2),
        "limit": unused_limit,
        "usage": ceil(float(unused_size) * 100.0 / float(unused_limit)),
        "space_left": max(unused_limit - unused_size, 0),
    }


def check_inactive_users():
    count = User.objects.exclude(requires_activation=User.ACTIVATION_NONE).count()
    return {"is_ok": count <= 10, "count": count}


def count_db_items():
    return {
        "attachments": Attachment.objects.count(),
        "attachments_total_size": get_total_attachment_storage_usage(),
        "attachments_unused_size": get_total_unused_attachments_size(),
        "threads": Thread.objects.count(),
        "posts": Post.objects.count(),
        "users": User.objects.count(),
    }
