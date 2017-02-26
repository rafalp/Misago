from rest_framework.response import Response

from misago.core.shortcuts import get_int_or_404
from misago.threads.viewmodels import (
    ForumThreads, PrivateThreads, PrivateThreadsCategory, ThreadsCategory, ThreadsRootCategory)


class ThreadsList(object):
    threads = None

    def __call__(self, request, **kwargs):
        page = get_int_or_404(request.query_params.get('page', 0))
        if page == 1:
            page = 0  # api allows explicit first page

        list_type = request.query_params.get('list', 'all')

        category = self.get_category(request, pk=request.query_params.get('category'))
        threads = self.get_threads(request, category, list_type, page)

        return Response(self.get_response_json(request, category, threads)['THREADS'])

    def get_category(self, request, pk=None):
        raise NotImplementedError('Threads list has to implement get_category(request, pk=None)')

    def get_threads(self, request, category, list_type, page):
        return self.threads(request, category, list_type, page)

    def get_response_json(self, request, category, threads):
        return threads.get_frontend_context()


class ForumThreadsList(ThreadsList):
    threads = ForumThreads

    def get_category(self, request, pk=None):
        if pk:
            return ThreadsCategory(request, pk=pk)
        else:
            return ThreadsRootCategory(request)


class PrivateThreadsList(ThreadsList):
    threads = PrivateThreads

    def get_category(self, request, pk=None):
        return PrivateThreadsCategory(request)


threads_list_endpoint = ForumThreadsList()
private_threads_list_endpoint = PrivateThreadsList()
