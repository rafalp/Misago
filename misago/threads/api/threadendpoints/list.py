from rest_framework.response import Response

from ....core.shortcuts import get_int_or_404
from ...viewmodels import (
    ForumThreads,
    PrivateThreads,
    PrivateThreadsCategory,
    ThreadsCategory,
    ThreadsRootCategory,
)


class ThreadsList:
    threads = None

    def __call__(self, request, **kwargs):
        start = get_int_or_404(request.query_params.get("start", 0))
        list_type = request.query_params.get("list", "all")
        category = self.get_category(request, pk=request.query_params.get("category"))
        threads = self.get_threads(request, category, list_type, start)

        return Response(self.get_response_json(request, category, threads)["THREADS"])

    def get_category(self, request, pk=None):
        raise NotImplementedError(
            "Threads list has to implement get_category(request, pk=None)"
        )

    def get_threads(self, request, category, list_type, start):
        return self.threads(  # pylint: disable=not-callable
            request, category, list_type, start
        )

    def get_response_json(self, request, category, threads):
        return threads.get_frontend_context()


class ForumThreadsList(ThreadsList):
    threads = ForumThreads

    def get_category(self, request, pk=None):
        if pk:
            return ThreadsCategory(request, pk=pk)
        return ThreadsRootCategory(request)


class PrivateThreadsList(ThreadsList):
    threads = PrivateThreads

    def get_category(self, request, pk=None):
        return PrivateThreadsCategory(request)


threads_list_endpoint = ForumThreadsList()
private_threads_list_endpoint = PrivateThreadsList()
