from datetime import timedelta

from unidecode import unidecode

from django.core.urlresolvers import resolve, reverse
from django.http import Http404
from django.template.defaultfilters import slugify as django_slugify
from django.utils import html, timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

import six


def slugify(string):
    string = six.text_type(string)
    string = unidecode(string)
    return django_slugify(string.replace('_', ' ').strip())


def format_plaintext_for_html(string):
    return html.linebreaks(html.urlize(html.escape(string)))


"""
Mark request as having sensitive parameters
We can't use decorator because of DRF uses custom HttpRequest
that is incompatibile with Django's decorator
"""
def hide_post_parameters(request):
    request.sensitive_post_parameters = '__ALL__'


"""
Return path utility
"""
def clean_return_path(request):
    if request.method == 'POST' and 'return_path' in request.POST:
        return _get_return_path_from_post(request)
    else:
        return _get_return_path_from_referer(request)


def _get_return_path_from_post(request):
    return_path = request.POST.get('return_path')
    try:
        if not return_path:
            raise ValueError()
        if not return_path.startswith('/'):
            raise ValueError()
        resolve(return_path)
        return return_path
    except (Http404, ValueError):
        return None


def _get_return_path_from_referer(request):
    referer = request.META.get('HTTP_REFERER')
    try:
        if not referer:
            raise ValueError()
        if not referer.startswith(request.scheme):
            raise ValueError()
        referer = referer[len(request.scheme) + 3:]
        if not referer.startswith(request.META['HTTP_HOST']):
            raise ValueError()
        referer = referer[len(request.META['HTTP_HOST'].rstrip('/')):]
        if not referer.startswith('/'):
            raise ValueError()
        resolve(referer)
        return referer
    except (Http404, KeyError, ValueError):
        return None


"""
Utils for resolving requests destination
"""
def _is_request_path_under_misago(request):
    # We are assuming that forum_index link is root of all Misago links
    forum_index = reverse('misago:index')
    path_info = request.path_info

    if len(forum_index) > len(path_info):
        return False
    return path_info[:len(forum_index)] == forum_index


def is_request_to_misago(request):
    try:
        return request._request_to_misago
    except AttributeError:
        request._request_to_misago = _is_request_path_under_misago(request)
        return request._request_to_misago


def is_referer_local(request):
    referer = request.META.get('HTTP_REFERER')

    if not referer:
        return False
    if not referer.startswith(request.scheme):
        return False
    referer = referer[len(request.scheme) + 3:]
    if not referer.startswith(request.META['HTTP_HOST']):
        return False
    referer = referer[len(request.META['HTTP_HOST'].rstrip('/')):]
    if not referer.startswith('/'):
        return False

    return True
