from django.http import Http404
from rest_framework.response import Response

from misago.threads.viewmodels.category import ThreadsRootCategory, ThreadsCategory
from misago.threads.viewmodels.threads import ForumThreads


class ListEndpointBase(object):
    category = None
    threads = None

    template_name = None

    def __call__(self, request, **kwargs):
        try:
            page = int(request.query_params.get('page', 0))
            if page == 1:
                page = 0 # api allows explicit first page
        except (ValueError, TypeError):
            raise Http404()

        list_type = request.query_params.get('list', 'all')

        category = self.get_category(request, pk=request.query_params.get('category'))
        threads = self.get_threads(request, category, list_type, page)

        return Response(self.get_response_json(request, category, threads)['THREADS'])

    def get_threads(self, request, category, list_type, page):
        return self.threads(request, category, list_type, page)

    def get_response_json(self, request, category, threads):
        return threads.get_frontend_context()


class ForumThreads(ListEndpointBase):
    threads = ForumThreads

    def get_category(self, request, pk=None):
        if pk:
            return ThreadsCategory(request, pk=pk)
        else:
            return ThreadsRootCategory(request)

threads_list_endpoint = ForumThreads()
