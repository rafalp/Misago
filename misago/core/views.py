from django.shortcuts import render
from django.utils import timezone
from django.views import i18n
from django.views.decorators.http import last_modified
from django.views.decorators.cache import cache_page

from misago.forums.lists import get_forums_list
from misago.users.online.ranks import get_ranks_online


def forum_index(request):
    return render(request, 'misago/index.html', {
        'categories': get_forums_list(request.user),
        'ranks_online': get_ranks_online(request.user),
    })


last_modified_date = timezone.now()

@cache_page(86400, key_prefix='js18n')
@last_modified(lambda req, **kw: last_modified_date)
def javascript_catalog(request):
    return i18n.javascript_catalog(request, 'djangojs', None)
