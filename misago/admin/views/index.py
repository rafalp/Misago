import json

import requests
from requests.exceptions import RequestException

from django.contrib.auth import get_user_model
from django.http import Http404, JsonResponse
from django.utils.translation import ugettext as _

from misago import __version__
from misago.core.cache import cache
from misago.threads.models import Post, Thread

from . import render


VERSION_CHECK_CACHE_KEY = "misago_version_check"

UserModel = get_user_model()


def admin_index(request):
    inactive_users_queryset = UserModel.objects.exclude(
        requires_activation=UserModel.ACTIVATION_NONE,
    )

    db_stats = {
        'threads': Thread.objects.count(),
        'posts': Post.objects.count(),
        'users': UserModel.objects.count(),
        'inactive_users': inactive_users_queryset.count()
    }

    return render(
        request, 'misago/admin/index.html', {
            'db_stats': db_stats,
            'version_check': cache.get(VERSION_CHECK_CACHE_KEY),
        }
    )


def check_version(request):
    if request.method != "POST":
        raise Http404()

    version = cache.get(VERSION_CHECK_CACHE_KEY, 'nada')

    if version == 'nada':
        try:
            api_url = 'https://api.github.com/repos/rafalp/Misago/releases'
            r = requests.get(api_url)

            if r.status_code != requests.codes.ok:
                r.raise_for_status()
            latest_version = json.loads(r.content)[0]['tag_name']

            latest = [int(v) for v in latest_version.split(".")]
            current = [int(v) for v in __version__.split(".")]

            for i in range(3):
                if latest[i] > current[i]:
                    message = _("Outdated: %(current)s < %(latest)s")
                    formats = {
                        'latest': latest_version,
                        'current': __version__,
                    }

                    version = {
                        'is_error': True,
                        'message': message % formats,
                    }
                    break
            else:
                formats = {
                    'current': __version__,
                }
                version = {
                    'is_error': False,
                    'message': _("Up to date! (%(current)s)") % formats,
                }

            cache.set(VERSION_CHECK_CACHE_KEY, version, 180)
        except (RequestException, IndexError, KeyError, ValueError):
            message = _("Failed to connect to GitHub API. Try again later.")
            version = {
                'is_error': True,
                'message': message,
            }

    return JsonResponse(version)
