from collections import OrderedDict

from django.http import Http404
from django.shortcuts import *  # noqa


def paginate(object_list, page, per_page, orphans=0,
             allow_empty_first_page=True,
             allow_explicit_first_page=False):
    from django.http import Http404
    from django.core.paginator import Paginator, EmptyPage
    from .exceptions import ExplicitFirstPage

    if page in (1, "1") and not allow_explicit_first_page:
        raise ExplicitFirstPage()
    elif not page:
        page = 1

    try:
        return Paginator(
            object_list, per_page, orphans=orphans,
            allow_empty_first_page=allow_empty_first_page).page(page)
    except EmptyPage:
        raise Http404()


def pagination_dict(page, include_page_range=True):
    pagination = {
        'page': page.number,
        'pages': page.paginator.num_pages,
        'page_range': None,
        'first': None,
        'previous': None,
        'next': None,
        'last': None,
        'before': 0,
        'more': 0,
    }

    if include_page_range:
        pagination['page_range'] = list(page.paginator.page_range)

    if page.has_previous():
        pagination['first'] = 1
        if page.previous_page_number() > 1:
            pagination['previous'] = page.previous_page_number()

    if page.has_next():
        pagination['last'] = page.paginator.num_pages
        if page.next_page_number() <= page.paginator.num_pages:
            pagination['next'] = page.next_page_number()

    if page.start_index():
        pagination['before'] = page.start_index() - 1
    pagination['more'] = page.paginator.count - page.end_index()

    return OrderedDict([
        ('count', page.paginator.count),
        ('page', pagination['page']),
        ('pages', pagination['pages']),
        ('page_range', pagination['page_range']),
        ('first', pagination['first']),
        ('previous', pagination['previous']),
        ('next', pagination['next']),
        ('last', pagination['last']),
        ('before', pagination['before']),
        ('more', pagination['more'])
    ])


def validate_slug(model, slug):
    from .exceptions import OutdatedSlug
    if model.slug != slug:
        raise OutdatedSlug(model)


def get_int_or_404(value):
    if unicode(value).isdigit():
        return int(value)
    else:
        raise Http404()
