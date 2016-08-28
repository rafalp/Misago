from django.shortcuts import get_object_or_404

from misago.acl import add_acl

from ..permissions.threads import exclude_invisible_posts


class ViewModel(object):
    def __init__(self, request, thread, pk, select_for_update=False):
        model = self.get_post(request, thread, pk, select_for_update)

        add_acl(request.user, model)

        self._model = model
        self._thread = model.thread
        self._category = model.category

    @property
    def model(self):
        return self._model

    @property
    def thread(self):
        return self._thread

    @property
    def category(self):
        return self._category

    def get_post(self, request, thread, pk, select_for_update=False):
        queryset = self.get_queryset(request, thread.model)
        if select_for_update:
            queryset = queryset.select_for_update()
        else:
            queryset = queryset.select_related(
                'poster',
                'poster__rank',
                'poster__ban_cache'
            )

        post = get_object_or_404(queryset, pk=pk)

        post.thread = thread.model
        post.category = thread.category

        return post

    def get_queryset(self, request, thread):
        return exclude_invisible_posts(request.user, thread.category, thread.post_set)


class ThreadPost(ViewModel):
    pass
