from django.shortcuts import redirect

from misago.forums.lists import get_forum_path

from misago.threads.views.generic.base import ViewBase


__all__ = ['ThreadView']


class ThreadView(ViewBase):
    """
    Basic view for threads
    """
    template = 'thread.html'

    def dispatch(self, request, *args, **kwargs):
        relations = ['forum', 'starter', 'last_poster', 'first_post']
        thread = self.fetch_thread(request, select_related=relations, **kwargs)
        forum = thread.forum

        self.check_forum_permissions(request, forum)
        self.check_thread_permissions(request, thread)

        return self.render(request, {
            'forum': forum,
            'path': get_forum_path(forum),
            'thread': thread
        })
