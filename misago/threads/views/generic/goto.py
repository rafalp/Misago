from django.http import Http404
from django.shortcuts import redirect

from misago.threads import goto
from misago.threads.views.generic.base import ViewBase


__all__ = ['BaseGotoView', 'GotoLastView', 'GotoNewView', 'GotoPostView']


class BaseGotoView(ViewBase):
    def get_redirect(self, user, thread):
        raise NotImplementedError("views inheriting form BaseGotoView "
                                  "should define get_redirect method")

    def dispatch(self, request, *args, **kwargs):
        thread = self.fetch_thread(request, select_related=['forum'], **kwargs)
        forum = thread.forum

        self.check_forum_permissions(request, forum)
        self.check_thread_permissions(request, thread)

        return redirect(self.get_redirect(request.user, thread))


class GotoLastView(BaseGotoView):
    def get_redirect(self, user, thread):
        return goto.last(user, thread)


class GotoNewView(BaseGotoView):
    def get_redirect(self, user, thread):
        return goto.new(user, thread)


class GotoPostView(BaseGotoView):
    def get_redirect(self, user, thread, post):
        return goto.post(user, thread, post)

    def dispatch(self, request, *args, **kwargs):
        post = self.fetch_post(
            request, select_related=['thread', 'forum'], **kwargs)
        forum = post.forum
        thread = post.thread

        self.check_forum_permissions(request, forum)
        thread.forum = forum
        self.check_thread_permissions(request, thread)
        self.check_post_permissions(request, post)

        return redirect(self.get_redirect(request.user, thread, post))
