from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from misago.models import Forum, Thread, Post
from misago.utils.pagination import make_pagination

class ViewBase(object):
    def __new__(cls, request, **kwargs):
        obj = super(ViewBase, cls).__new__(cls)
        return obj(request, **kwargs)
        
    def set_forum_context(self):
        pass

    def set_thread_context(self):
        self.thread = Thread.objects.get(pk=self.kwargs.get('thread'))
        self.forum = self.thread.forum
        self.proxy = Forum.objects.parents_aware_forum(self.forum)
        self.request.acl.forums.allow_forum_view(self.forum)
        self.request.acl.threads.allow_thread_view(self.request.user, self.thread)

    def set_post_contex(self):
        pass

    def redirect_to_post(self, post):
        pagination = make_pagination(0, self.request.acl.threads.filter_posts(self.request, self.thread, self.thread.post_set).filter(id__lte=post.pk).count(), self.request.settings.posts_per_page)
        if pagination['total'] > 1:
            return redirect(reverse(self.thread_url, kwargs={'thread': self.thread.pk, 'slug': self.thread.slug, 'page': pagination['total']}) + ('#post-%s' % post.pk))
        return redirect(reverse(self.thread_url, kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}) + ('#post-%s' % post.pk))
