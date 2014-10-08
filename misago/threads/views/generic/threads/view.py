from misago.core.shortcuts import paginate

from misago.threads.views.generic.base import ViewBase


__all__ = ['ThreadsView']


class ThreadsView(ViewBase):
    def get_threads(self, request, kwargs):
        queryset = self.get_threads_queryset(request, forum)
        queryset = threads_qs.order_by('-last_post_id')

        page = paginate(threads_qs, kwargs.get('page', 0), 30, 10)
        threads = [thread for thread in page.object_list]

        return page, threads

    def get_threads_queryset(self, request):
        return forum.thread_set.all().order_by('-last_post_id')

    def clean_kwargs(self, request, kwargs):
        cleaned_kwargs = kwargs.copy()
        if request.user.is_anonymous():
            """we don't allow sort/filter for guests"""
            cleaned_kwargs.pop('sort', None)
            cleaned_kwargs.pop('show', None)
        return cleaned_kwargs
