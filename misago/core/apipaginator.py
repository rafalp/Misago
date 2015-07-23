from django.core.paginator import InvalidPage, Paginator as DjangoPaginator
from rest_framework.compat import OrderedDict
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class BaseApiPaginator(PageNumberPagination):
    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        paginator = DjangoPaginator(
            queryset, self.page_size, orphans=self.page_orphans)
        page_number = request.query_params.get(self.page_query_param, 1)

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=six.text_type(exc)
            )
            raise NotFound(msg)

        if paginator.count > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_meta(self):
        pagination = {
            'pages': self.page.paginator.num_pages,
            'first': None,
            'previous': None,
            'next': None,
            'last': None,
            'before': 0,
            'more': 0,
        }

        if self.page.has_previous():
            pagination['first'] = 1
            if self.page.previous_page_number() > 1:
                pagination['previous'] = self.page.previous_page_number()

        if self.page.has_next():
            pagination['last'] = self.page.paginator.num_pages
            if self.page.next_page_number() < self.page.paginator.num_pages:
                pagination['next'] = self.page.next_page_number()

        if self.page.start_index():
            pagination['before'] = self.page.start_index() - 1
        pagination['more'] = self.page.paginator.count - self.page.end_index()

        return OrderedDict([
            ('count', self.page.paginator.count),
            ('pages', pagination['pages']),
            ('first', pagination['first']),
            ('previous', pagination['previous']),
            ('next', pagination['next']),
            ('last', pagination['last']),
            ('before', pagination['before']),
            ('more', pagination['more'])
        ])

    def get_paginated_response(self, data):
        response_data = self.get_meta()
        response_data['results'] = data
        return Response(response_data)


def ApiPaginator(per_page=None, orphans=0):
    return type('ApiPaginator', (BaseApiPaginator, ), {
        'page_size': per_page,
        'page_orphans': orphans
    })
