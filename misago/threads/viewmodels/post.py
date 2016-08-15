from django.shortcuts import get_object_or_404

from misago.acl import add_acl

from ..permissions.threads import allow_see_post, exclude_invisible_posts


class ViewModel(object):
    def __init__(self, request, thread, pk):
        post = self.get_post(request, thread, pk)

        add_acl(request.user, post)

        self.post = post

    def get_post(self, request, thread, pk):
        queryset = self.get_queryset(request, thread.thread)
        post = get_object_or_404(queryset, pk=pk, is_event=False)

        post.category = thread.category

        allow_see_post(request.user, post)

        return post

    def get_queryset(self, request, thread):
        queryset = thread.post_set.select_related(
            'poster',
            'poster__rank',
            'poster__ban_cache'
        )
        return exclude_invisible_posts(request.user, thread.category, queryset)


class ThreadPost(ViewModel):
    pass
