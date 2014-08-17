"""
Module with basic views for use by inheriting actions
"""
from django.shortcuts import render
from django.views.generic import View

from misago.acl import add_acl
from misago.core.shortcuts import get_object_or_404, paginate, validate_slug
from misago.forums.lists import get_forums_list, get_forum_path
from misago.forums.models import Forum
from misago.forums.permissions import allow_see_forum, allow_browse_forum


class ForumMixin(object):
    """
    Mixin for getting forums
    """
    def get_forum(self, request, **kwargs):
        forum = self.fetch_forum(request, **kwargs)
        self.check_forum_permissions(request, forum)

        if kwargs.get('forum_slug'):
            validate_slug(forum, kwargs.get('forum_slug'))

        return forum

    def fetch_forum(self, request, **kwargs):
        return get_object_or_404(
            Forum, id=kwargs.get('forum_id'), role='forum')

    def check_forum_permissions(self, request, forum):
        add_acl(request.user, forum)
        allow_see_forum(request.user, forum)
        allow_browse_forum(request.user, forum)


class ViewBase(ForumMixin, View):
    templates_dir = ''
    template = ''

    def final_template(self):
        return '%s/%s' % (self.templates_dir, self.template)

    def process_context(self, request, context):
        """
        Simple hook for extending and manipulating template context.
        """
        return context

    def render(self, request, context=None, template=None):
        context = self.process_context(request, context or {})
        template = template or self.final_template()
        return render(request, template, context)


class ForumView(ViewBase):
    """
    Basic view for threads lists
    """
    template = 'list.html'

    def get_threads(self, request, forum, **kwargs):
        return forum.thread_set

    def dispatch(self, request, *args, **kwargs):
        forum = self.get_forum(request, **kwargs)
        forum.subforums = get_forums_list(request.user, forum)
        threads = self.get_threads(request, forum, **kwargs)

        return self.render(request, {
            'forum': forum,
            'path': get_forum_path(forum),
        })


class ThreadView(ViewBase):
    """
    Basic view for threads
    """
    def fetch_thread(self, request, **kwargs):
        pass

    def dispatch(self, request, *args, **kwargs):
        thread = self.fetch_thread(request, **kwargs)


class PostView(ViewBase):
    """
    Basic view for posts
    """
    def fetch_post(self, request, **kwargs):
        pass

    def dispatch(self, request, *args, **kwargs):
        post = self.fetch_post(request, **kwargs)


class EditorView(ViewBase):
    """
    Basic view for starting/replying/editing
    """
    pass
