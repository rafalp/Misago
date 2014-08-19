"""
Module with basic views for use by inheriting actions
"""
from django.db.transaction import atomic
from django.shortcuts import redirect, render
from django.views.generic import View

from misago.acl import add_acl
from misago.core.shortcuts import get_object_or_404, paginate, validate_slug
from misago.forums.lists import get_forums_list, get_forum_path
from misago.forums.models import Forum
from misago.forums.permissions import allow_see_forum, allow_browse_forum

from misago.threads.forms.posting import EditorFormset, START, REPLY, EDIT
from misago.threads.models import Thread, Post
from misago.threads.permissions import allow_see_thread, allow_start_thread


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

    def fetch_thread(self, request, lock=False, **kwargs):
        queryset = Thread.objects
        if lock:
            queryset = queryset.select_for_update()

        return get_object_or_404(queryset, id=kwargs.get('thread_id'))

    def check_thread_permissions(self, request, thread):
        add_acl(request.user, thread)
        allow_see_thread(request.user, thread)


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
    template = 'editor.html'

    def find_mode(self, request, *args, **kwargs):
        """
        First step: guess from request what kind of view we are
        """
        is_post = request.method == 'POST'

        if 'forum_id' in kwargs:
            mode = START
            user = request.user

            forum = self.get_forum(request, lock=is_post, **kwargs)
            thread = Thread(forum=forum, starter=user, last_poster=user)
            post = Post(forum=forum, thread=thread, poster=user)
            quote = Post(0)
        elif 'thread_id' in kwargs:
            thread = self.get_thread(request, lock=is_post, **kwargs)
            forum = thread.forum

        return mode, forum, thread, post, quote

    def allow_mode(self, user, mode, forum, thread, post, quote):
        """
        Second step: check start/reply/edit permissions
        """
        if mode == START:
            self.allow_start(user, forum)
        if mode == REPLY:
            self.allow_reply(user, forum, thread, quote)
        if mode == EDIT:
            self.allow_edit(user, forum, thread, post)

    def allow_start(self, user, forum):
        allow_start_thread(user, forum)

    def allow_reply(self, user, forum, thread, quote):
        raise NotImplementedError()

    def allow_edit(self, user, forum, thread, post):
        raise NotImplementedError()

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            with atomic():
                return self.real_dispatch(request, *args, **kwargs)
        else:
            return self.real_dispatch(request, *args, **kwargs)

    def real_dispatch(self, request, *args, **kwargs):
        mode_context = self.find_mode(request, *args, **kwargs)
        self.allow_mode(request.user, *mode_context)

        mode, forum, thread, post, quote = mode_context
        formset = EditorFormset(request=request,
                                mode=mode,
                                user=request.user,
                                forum=forum,
                                thread=thread,
                                post=post,
                                quote=quote)

        if request.method == 'POST':
            if 'submit' in request.POST and formset.is_valid():
                formset.save()
                return redirect('misago:index')
            else:
                formset.update()

        return self.render(request, {
            'mode': mode,
            'formset': formset,
            'forms': formset.get_forms_list(),
            'main_forms': formset.get_main_forms(),
            'supporting_forms': formset.get_supporting_forms(),
            'forum': forum,
            'path': get_forum_path(forum),
            'thread': thread,
            'post': post,
            'quote': quote
        })
