from django.http import Http404
from django.shortcuts import redirect

from misago.threads import goto
from misago.threads.views.generic.base import ViewBase


__all__ = [
    'BaseGotoView',
    'GotoLastView',
    'GotoNewView',
    'GotoPostView'
]


class BaseGotoView(ViewBase):
    def get_redirect(self, user, thread):
        raise NotImplementedError("views inheriting form BaseGotoView "
                                  "should define get_redirect method")

    def dispatch(self, request, *args, **kwargs):
        thread = self.fetch_thread(request, select_related=['forum'], **kwargs)
        forum = thread.forum

        self.check_forum_permissions(request, forum)
        self.check_thread_permissions(request, thread)

        posts_qs = self.exclude_invisible_posts(
            thread.post_set, request.user, forum, thread)

        return redirect(self.get_redirect(request.user, thread, posts_qs))


class GotoLastView(BaseGotoView):
    def get_redirect(self, user, thread, posts_qs):
        return goto.last(thread, posts_qs)


class GotoNewView(BaseGotoView):
    def get_redirect(self, user, thread, posts_qs):
        return goto.new(user, thread, posts_qs)


class GotoPostView(BaseGotoView):
    def get_redirect(self, thread, posts_qs, post):
        return goto.post(thread, posts_qs, post)

    def dispatch(self, request, *args, **kwargs):
        post = self.fetch_post(
            request, select_related=['thread', 'forum'], **kwargs)
        forum = post.forum
        thread = post.thread

        self.check_forum_permissions(request, forum)
        thread.forum = forum
        self.check_thread_permissions(request, thread)
        self.check_post_permissions(request, post)

        posts_qs = self.exclude_invisible_posts(
            thread.post_set, request.user, thread.forum, thread)

        return redirect(self.get_redirect(thread, posts_qs, post))
