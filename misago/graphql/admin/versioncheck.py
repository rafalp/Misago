import requests
from ariadne import QueryType
from django.core.cache import cache
from django.utils.translation import gettext as _
from requests.exceptions import RequestException

from ... import __released__, __version__
from .status import Status

CACHE_KEY = "misago_admin_version_check"
CACHE_LENGTH = 3600 * 8  # 4 hours

version_check = QueryType()


@version_check.field("version")
def resolve_version(*_):
    if not __released__:
        return get_unreleased_error()

    data = cache.get(CACHE_KEY)
    if not data:
        data = check_version_with_api()
        if data["status"] != Status.WARNING:
            cache.set(CACHE_KEY, data, CACHE_LENGTH)
    return data


def get_unreleased_error():
    return {
        "status": Status.ERROR,
        "message": _("The site is running using unreleased version of Misago."),
        "description": _(
            "Unreleased versions of Misago can lack security features and there is "
            "no supported way to upgrade them to release versions later."
        ),
    }


def check_version_with_api():
    try:
        latest_version = get_latest_version()
        return compare_versions(__version__, latest_version)
    except (RequestException, KeyError, ValueError):
        return {
            "status": Status.WARNING,
            "message": _("Failed to connect to pypi.org API. Try again later."),
            "description": _(
                "Version check feature relies on the API operated by the Python "
                "Package Index (pypi.org) API to retrieve latest Misago release "
                "version."
            ),
        }


def get_latest_version():
    api_url = "https://pypi.org/pypi/Misago/json"
    r = requests.get(api_url)
    r.raise_for_status()
    return r.json()["info"]["version"]


def compare_versions(current, latest):
    if latest == current:
        return {
            "status": Status.SUCCESS,
            "message": _("The site is running updated version of Misago."),
            "description": _("Misago %(version)s is latest release.")
            % {"version": current},
        }

    return {
        "status": Status.ERROR,
        "message": _("The site is running outdated version of Misago."),
        "description": _(
            "The site is running Misago version %(version)s while version %(latest)s "
            "is available."
        )
        % {"version": current, "latest": latest},
    }
