from rest_framework import viewsets
from rest_framework.response import Response

from misago.core.shortcuts import get_int_or_404
from misago.threads.viewmodels.posts import ThreadPosts
from misago.threads.viewmodels.thread import ForumThread


class ViewSet(viewsets.ViewSet):
    thread = None
    posts = None

    def get_thread(self, request, pk):
        return self.thread(request, get_int_or_404(pk))

    def get_posts(self, request, thread, page):
        return self.posts(request, thread, page)

    def list(self, request, thread_pk):
        page = get_int_or_404(request.query_params.get('page', 0))
        if page == 1:
            page = 0 # api allows explicit first page

        thread = self.get_thread(request, thread_pk)
        posts = self.get_posts(request, thread, page)

        data = thread.get_frontend_context()
        data['post_set'] = posts.get_frontend_context()

        return Response(data)


class ThreadPostsViewSet(ViewSet):
    thread = ForumThread
    posts = ThreadPosts
