from django.shortcuts import get_object_or_404

from misago.acl import add_acl
from misago.core.viewmodel import ViewModel as BaseViewModel
from misago.threads.permissions import exclude_invisible_posts


class ViewModel(BaseViewModel):
    def __init__(self, request, thread, pk):
        model = self.get_post(request, thread, pk)

        add_acl(request.user, model)

        self._model = model

    def get_post(self, request, thread, pk):
        try:
            thread_model = thread.unwrap()
        except AttributeError:
            thread_model = thread

        queryset = self.get_queryset(request, thread_model).select_related(
            'poster',
            'poster__rank',
            'poster__ban_cache',
        )

        post = get_object_or_404(queryset, pk=pk)

        post.thread = thread_model
        post.category = thread.category

        return post

    def get_queryset(self, request, thread):
        return exclude_invisible_posts(request.user, thread.category, thread.post_set)


class ThreadPost(ViewModel):
    pass
