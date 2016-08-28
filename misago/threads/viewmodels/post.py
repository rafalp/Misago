from django.shortcuts import get_object_or_404

from misago.acl import add_acl

from ..permissions.threads import exclude_invisible_posts


class ViewModel(object):
    def __init__(self, request, thread, pk, select_for_update=False):
        post = self.get_post(request, thread, pk, select_for_update)

        add_acl(request.user, post)

        self.post = post

    def get_post(self, request, thread, pk, select_for_update=False):
        queryset = self.get_queryset(request, thread.thread)
        if select_for_update:
            queryset = queryset.select_for_update()
        else:
            queryset = queryset.select_related(
                'poster',
                'poster__rank',
                'poster__ban_cache'
            )

        post = get_object_or_404(queryset, pk=pk)

        post.thread = thread.thread
        post.category = thread.category

        return post

    def get_queryset(self, request, thread):
        return exclude_invisible_posts(request.user, thread.category, thread.post_set)


class ThreadPost(ViewModel):
    pass
