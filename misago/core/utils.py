from datetime import timedelta

from unidecode import unidecode

from django.http import Http404
from django.core.urlresolvers import resolve, reverse
from django.template.defaultfilters import slugify as django_slugify
from django.utils.translation import ugettext_lazy as _, ungettext_lazy


def slugify(string):
    string = unicode(string)
    string = unidecode(string)
    return django_slugify(string.replace('_', ' ').strip())


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


"""
Utility that humanizes time amount.

Expects number of seconds as first argument
"""
def time_amount(value):
    delta = timedelta(seconds=value)

    units_dict = {
        'd': delta.days,
        'h': 0,
        'm': 0,
        's': delta.seconds,
    }

    if units_dict['s'] >= 3600:
        units_dict['h'] = units_dict['s'] / 3600
        units_dict['s'] -= units_dict['h'] * 3600

    if units_dict['s'] >= 60:
        units_dict['m'] = units_dict['s'] / 60
        units_dict['s'] -= units_dict['m'] * 60

    precisions = []

    if units_dict['d']:
        string = ungettext_lazy(
            '%(days)s day', '%(days)s days', units_dict['d'])
        precisions.append(string % {'days': units_dict['d']})

    if units_dict['h']:
        string = ungettext_lazy(
            '%(hours)s hour', '%(hours)s hours', units_dict['h'])
        precisions.append(string % {'hours': units_dict['h']})

    if units_dict['m']:
        string = ungettext_lazy(
            '%(minutes)s minute', '%(minutes)s minutes', units_dict['m'])
        precisions.append(string % {'minutes': units_dict['m']})

    if units_dict['s']:
        string = ungettext_lazy(
            '%(seconds)s second', '%(seconds)s seconds', units_dict['s'])
        precisions.append(string % {'seconds': units_dict['s']})

    if not precisions:
        precisions.append(_("0 seconds"))

    if len(precisions) == 1:
        return precisions[0]
    else:
        formats = {
            'first_part': ', '.join(precisions[:-1]),
            'and_part': precisions[-1],
        }

        return _("%(first_part)s and %(and_part)s") % formats


"""
MD subset for use for enchancing items descriptions
"""
MD_SUBSET_FORBID_SYNTAX = (
    # References are evil
    'reference', 'reference', 'image_reference', 'short_reference',

    # Blocks are evil too
    'hashheader', 'setextheader', 'code', 'quote', 'hr', 'olist', 'ulist',
)
