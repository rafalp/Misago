from django.shortcuts import get_object_or_404

from ...acl.objectacl import add_acl_to_obj
from ...core.viewmodel import ViewModel as BaseViewModel
from ..permissions import exclude_invisible_posts

__all__ = ["ThreadPost"]


class ViewModel(BaseViewModel):
    def __init__(self, request, thread, pk):
        model = self.get_post(request, thread, pk)

        add_acl_to_obj(request.user_acl, model)

        self._model = model

    def get_post(self, request, thread, pk):
        try:
            thread_model = thread.unwrap()
        except AttributeError:
            thread_model = thread

        queryset = self.get_queryset(request, thread_model).select_related(
            "poster", "poster__rank", "poster__ban_cache"
        )

        post = get_object_or_404(queryset, pk=pk)

        post.thread = thread_model
        post.category = thread.category

        return post

    def get_queryset(self, request, thread):
        return exclude_invisible_posts(
            request.user_acl, thread.category, thread.post_set
        )


class ThreadPost(ViewModel):
    pass
