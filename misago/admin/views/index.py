from datetime import timedelta

import requests
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.http import Http404, JsonResponse
from django.utils import timezone
from django.utils.translation import gettext as _
from requests.exceptions import RequestException

from . import render
from ... import __released__, __version__
from ...conf import settings
from ...threads.models import Post, Thread, Attachment
from ...users.models import DataDownload

VERSION_CHECK_CACHE_KEY = "misago_version_check"

User = get_user_model()


def admin_index(request):
    totals = count_db_items()
    checks = {
        "address": check_misago_address(request),
        "cache": check_cache(),
        "data_downloads": check_data_downloads(),
        "debug": check_debug_status(),
        "https": check_https(request),
        "released": check_release_status(),
        "inactive_users": check_inactive_users(totals["inactive_users"]),
    }

    return render(
        request,
        "misago/admin/dashboard/index.html",
        {
            "totals": totals,
            "checks": checks,
            "all_ok": all([c["is_ok"] for c in checks.values()]),
            "version_check": cache.get(VERSION_CHECK_CACHE_KEY),
        },
    )


def check_cache():
    cache.set("misago_cache_test", "ok")
    return {"is_ok": cache.get("misago_cache_test") == "ok"}


def check_debug_status():
    return {"is_ok": not settings.DEBUG}


def check_https(request):
    return {"is_ok": request.is_secure()}


def check_release_status():
    return {"is_ok": __released__}


def check_misago_address(request):
    set_address = settings.MISAGO_ADDRESS
    correct_address = request.build_absolute_uri("/")

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


def check_inactive_users(inactive_count):
    return {"is_ok": inactive_count <= 10, "count": inactive_count}


def count_db_items():
    return {
        "attachments": Attachment.objects.count(),
        "threads": Thread.objects.count(),
        "posts": Post.objects.count(),
        "users": User.objects.count(),
        "inactive_users": User.objects.exclude(
            requires_activation=User.ACTIVATION_NONE
        ).count(),
    }


def check_version(request):
    if request.method != "POST":
        raise Http404()

    version = cache.get(VERSION_CHECK_CACHE_KEY, "nada")

    if version == "nada":
        try:
            api_url = "https://pypi.org/pypi/Misago/json"
            r = requests.get(api_url)
            r.raise_for_status()

            latest_version = r.json()["info"]["version"]

            if latest_version == __version__:
                version = {
                    "is_error": False,
                    "message": _("Up to date! (%(current)s)")
                    % {"current": __version__},
                }
            else:
                version = {
                    "is_error": True,
                    "message": _("Outdated: %(current)s! (latest: %(latest)s)")
                    % {"latest": latest_version, "current": __version__},
                }

            cache.set(VERSION_CHECK_CACHE_KEY, version, 180)
        except (RequestException, IndexError, KeyError, ValueError):
            version = {
                "is_error": True,
                "message": _("Failed to connect to pypi.org API. Try again later."),
            }

    return JsonResponse(version)
