from rest_framework.response import Response

from django.http import Http404

import six


def paginate(
        object_list,
        page,
        per_page,
        orphans=0,
        allow_empty_first_page=True,
        allow_explicit_first_page=False,
        paginator=None
):
    from django.core.paginator import Paginator, EmptyPage, InvalidPage
    from .exceptions import ExplicitFirstPage

    if page in (1, "1") and not allow_explicit_first_page:
        raise ExplicitFirstPage()
    elif not page:
        page = 1

    paginator = paginator or Paginator

    try:
        return paginator(
            object_list, per_page, orphans=orphans, allow_empty_first_page=allow_empty_first_page
        ).page(page)
    except (EmptyPage, InvalidPage):
        raise Http404()


def pagination_dict(page):
    pagination = {
        'page': page.number,
        'pages': page.paginator.num_pages,
        'count': page.paginator.count,
        'first': None,
        'previous': None,
        'next': None,
        'last': None,
        'before': 0,
        'more': 0,
    }

    if page.has_previous():
        pagination['first'] = 1
        pagination['previous'] = page.previous_page_number()

    if page.has_next():
        pagination['last'] = page.paginator.num_pages
        pagination['next'] = page.next_page_number()

    if page.start_index():
        pagination['before'] = page.start_index() - 1
    pagination['more'] = page.paginator.count - page.end_index()

    return pagination


def paginated_response(page, serializer=None, data=None, extra=None):
    response_data = pagination_dict(page)

    results = list(data or page.object_list)
    if serializer:
        results = serializer(results, many=True).data

    response_data.update({'results': results})

    if extra:
        response_data.update(extra)

    return Response(response_data)


def validate_slug(model, slug):
    from .exceptions import OutdatedSlug
    if model.slug != slug:
        raise OutdatedSlug(model)


def get_int_or_404(value):
    if six.text_type(value).isdigit():
        return int(value)
    else:
        raise Http404()
