from django.shortcuts import redirect
from django.utils import timezone
from django.views import i18n
from django.views.decorators.cache import cache_page
from django.views.decorators.http import last_modified


def forum_index(request):
    return  # blow up as this view is normally non-reachable!


def home_redirect(*args, **kwargs):
    return redirect('misago:index')


@cache_page(86400 * 2, key_prefix='misagojsi18n')
@last_modified(lambda req, **kw: timezone.now())
def javascript_catalog(request):
    return i18n.javascript_catalog(request, 'djangojs', None)
