from django.core.paginator import Paginator as DjangoPaginator, InvalidPage
from django.utils import six

from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .shortcuts import pagination_dict


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
        return pagination_dict(self.page)

    def get_paginated_response(self, data):
        response_data = self.get_meta()
        response_data['results'] = data
        return Response(response_data)


def ApiPaginator(per_page=None, orphans=0):
    return type('ApiPaginator', (BaseApiPaginator, ), {
        'page_size': per_page,
        'page_orphans': orphans
    })
