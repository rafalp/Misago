from django.shortcuts import get_object_or_404

from misago.acl import add_acl
from misago.core.viewmodel import ViewModel as BaseViewModel
from misago.threads.permissions import exclude_invisible_posts


__all__ = ['ThreadPost']


class ViewModel(BaseViewModel):
    def __init__(self, request, thread, pk, select_for_update=False):
        model = self.get_post(request, thread, pk, select_for_update)

        add_acl(request.user, model)

        self._model = model

    def get_post(self, request, thread, pk, select_for_update=False):
        try:
            thread_model = thread.unwrap()
        except AttributeError:
            thread_model = thread

        queryset = self.get_queryset(request, thread_model)
        if select_for_update:
            queryset = queryset.select_for_update()
        else:
            queryset = queryset.select_related('poster', 'poster__rank', 'poster__ban_cache')

        post = get_object_or_404(queryset, pk=pk)

        post.thread = thread_model
        post.category = thread.category

        return post

    def get_queryset(self, request, thread):
        return exclude_invisible_posts(request.user, thread.category, thread.post_set)


class ThreadPost(ViewModel):
    pass
