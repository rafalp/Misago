from django.shortcuts import render
from django.views.generic import View

from misago.acl import add_acl
from misago.core.shortcuts import get_object_or_404, validate_slug
from misago.forums.models import Forum
from misago.forums.permissions import allow_see_forum, allow_browse_forum

from misago.threads.models import Thread, Post
from misago.threads.permissions import allow_see_thread, allow_see_post


__all__ = ['ForumMixin', 'ThreadMixin', 'PostMixin', 'ViewBase']


class ForumMixin(object):
    """
    Mixin for getting forums
    """
    def get_forum(self, request, lock=False, **kwargs):
        forum = self.fetch_forum(request, lock, **kwargs)
        self.check_forum_permissions(request, forum)

        if kwargs.get('forum_slug'):
            validate_slug(forum, kwargs.get('forum_slug'))

        return forum

    def fetch_forum(self, request, lock=False, **kwargs):
        queryset = Forum.objects
        if lock:
            queryset = queryset.select_for_update()

        return get_object_or_404(
            queryset, id=kwargs.get('forum_id'), role='forum')

    def check_forum_permissions(self, request, forum):
        add_acl(request.user, forum)
        allow_see_forum(request.user, forum)
        allow_browse_forum(request.user, forum)


class ThreadMixin(object):
    """
    Mixin for getting thread
    """
    def get_thread(self, request, lock=False, **kwargs):
        thread = self.fetch_thread(request, lock, **kwargs)
        self.check_thread_permissions(request, thread)

        if kwargs.get('thread_slug'):
            validate_slug(thread, kwargs.get('thread_slug'))

        return thread

    def fetch_thread(self, request, lock=False, select_related=None,
                     queryset=None, **kwargs):
        queryset = queryset or Thread.objects
        if lock:
            queryset = queryset.select_for_update()
        if select_related:
            queryset = queryset.select_related(*select_related)

        return get_object_or_404(queryset, id=kwargs.get('thread_id'))

    def check_thread_permissions(self, request, thread):
        add_acl(request.user, thread)
        allow_see_thread(request.user, thread)


class PostMixin(object):
    def get_post(self, request, lock=False, **kwargs):
        thread = self.fetch_post(request, lock, **kwargs)
        self.check_post_permissions(request, thread)

        return thread

    def fetch_post(self, request, lock=False, select_related=None,
                   queryset=None, **kwargs):
        queryset = queryset or Post.objects
        if lock:
            queryset = queryset.select_for_update()
        if select_related:
            queryset = queryset.select_related(*select_related)

        return get_object_or_404(queryset, id=kwargs.get('post_id'))

    def check_post_permissions(self, request, post):
        add_acl(request.user, post)
        allow_see_post(request.user, post)


class ViewBase(ForumMixin, ThreadMixin, PostMixin, View):
    def process_context(self, request, context):
        """
        Simple hook for extending and manipulating template context.
        """
        return context

    def render(self, request, context=None, template=None):
        context = self.process_context(request, context or {})
        template = template or self.template
        return render(request, template, context)
