import requests
from requests.exceptions import RequestException

from django.contrib.auth import get_user_model
from django.http import Http404, JsonResponse
from django.utils.translation import ugettext as _

from misago import __version__
from misago.conf import settings
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
            'address_check': check_misago_address(request),
            'version_check': cache.get(VERSION_CHECK_CACHE_KEY),
        }
    )


def check_misago_address(request):
    set_address = settings.MISAGO_ADDRESS
    correct_address = request.build_absolute_uri('/')

    return {
        'is_correct': set_address == correct_address,
        'set_address': set_address,
        'correct_address': correct_address,
    }


def check_version(request):
    if request.method != "POST":
        raise Http404()

    version = cache.get(VERSION_CHECK_CACHE_KEY, 'nada')

    if version == 'nada':
        try:
            api_url = 'https://pypi.org/pypi/Misago/json'
            r = requests.get(api_url)
            r.raise_for_status()

            latest_version = r.json()['info']['version']

            if latest_version == __version__:
                version = {
                    'is_error': False,
                    'message': _("Up to date! (%(current)s)") % {
                        'current': __version__,
                    },
                }
            else:
                version = {
                    'is_error': True,
                    'message': _("Outdated: %(current)s! (latest: %(latest)s)") % {
                        'latest': latest_version,
                        'current': __version__,
                    },
                }

            cache.set(VERSION_CHECK_CACHE_KEY, version, 180)
        except (RequestException, IndexError, KeyError, ValueError) as e:
            version = {
                'is_error': True,
                'message': _("Failed to connect to pypi.org API. Try again later."),
            }

    return JsonResponse(version)
