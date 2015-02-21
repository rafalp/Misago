from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.utils import timezone
from django.views import i18n
from django.views.decorators.http import last_modified
from django.views.decorators.cache import cache_page, never_cache
from django.views.decorators.debug import sensitive_post_parameters

from misago.forums.lists import get_forums_list
from misago.users.online.ranks import get_ranks_online


def forum_index(request):
    return render(request, 'misago/index.html', {
        'categories': get_forums_list(request.user),
        'ranks_online': get_ranks_online(request.user),
    })


@cache_page(86400, key_prefix='js18n')
@last_modified(lambda req, **kw: timezone.now())
def javascript_catalog(request):
    return i18n.javascript_catalog(request, 'djangojs', None)


@never_cache
def preload_data(request):
    if not (settings.DEBUG or settings._MISAGO_JS_DEBUG):
        raise Http404()

    return render(request, 'misago/preloaded_data.js',
                  content_type='application/javascript')


def noscript(request, title=None, message=None):
    return render(request, 'misago/noscript.html', {
        'title': title,
        'message': message,
    })
