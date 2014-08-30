from django.contrib import messages
from django.db.models import Q
from django.db.transaction import atomic
from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy, ugettext as _
from django.views.generic import View

from misago.forums.lists import get_forum_path

from misago.threads.posting import (PostingInterrupt, EditorFormset,
                                    START, REPLY, EDIT)
from misago.threads.models import ANNOUNCEMENT, Thread, Post
from misago.threads.permissions import allow_start_thread
from misago.threads.views.generic.base import ViewBase


__all__ = ['EditorView']


class EditorView(ViewBase):
    """
    Basic view for starting/replying/editing
    """
    template = 'misago/posting/form.html'

    def find_mode(self, request, *args, **kwargs):
        """
        First step: guess from request what kind of view we are
        """
        is_post = request.method == 'POST'

        if 'forum_id' in kwargs:
            mode = START
            user = request.user

            forum = self.get_forum(request, lock=is_post, **kwargs)
            thread = Thread(forum=forum)
            post = Post(forum=forum, thread=thread)
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
                try:
                    formset.save()
                    return redirect(thread.get_absolute_url())
                except PostingInterrupt as e:
                    messages.error(request, e.message)
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
            'quote': quote,
        })
