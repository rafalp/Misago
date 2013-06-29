from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from misago.conf import settings
from misago.models import Forum, Thread, Post
from misago.utils.pagination import page_number

class ViewBase(object):
    def __new__(cls, request, **kwargs):
        obj = super(ViewBase, cls).__new__(cls)
        return obj(request, **kwargs)
        
    def _type_available(self):
        try:
            if not self.type_available():
                raise Http404()
        except AttributeError:
            pass

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

    def check_forum_type(self):
        type_prefix = self.type_prefix
        if type_prefix == 'thread':
            type_prefix = 'root'
        else:
            type_prefix = '%ss' % type_prefix
        try:
            if self.parents[0].parent_id != Forum.objects.special_pk(type_prefix):
                raise Http404()
        except (AttributeError, IndexError):
            if self.forum.special != type_prefix:
                raise Http404()

    def _check_permissions(self):
        try:
            self.check_permissions()
        except AttributeError:
            pass

    def redirect_to_post(self, post, type_prefix=None):
        type_prefix = type_prefix or self.type_prefix
        queryset = self.request.acl.threads.filter_posts(self.request, self.thread, self.thread.post_set)
        page = page_number(queryset.filter(id__lte=post.pk).count(), queryset.count(), settings.posts_per_page)
        if page > 1:
            return redirect(reverse(type_prefix, kwargs={'thread': self.thread.pk, 'slug': self.thread.slug, 'page': page}) + ('#post-%s' % post.pk))
        return redirect(reverse(type_prefix, kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}) + ('#post-%s' % post.pk))

    def template_vars(self, context):
        return context

    def retreat_redirect(self):
        if self.request.POST.get('retreat'):
            return redirect(self.request.POST.get('retreat'))
        return redirect(reverse(self.type_prefix, kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}))