from django.contrib import messages
from django.db.transaction import atomic
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _
from django.views.generic import View

from misago.core.exceptions import AjaxError
from misago.forums.lists import get_forum_path

from misago.threads import goto
from misago.threads.posting import (PostingInterrupt, EditorFormset,
                                    START, REPLY, EDIT)
from misago.threads.models import Thread, Post, Label
from misago.threads.permissions import allow_start_thread, allow_reply_thread
from misago.threads.views.generic.base import ViewBase


__all__ = ['EditorView']


class EditorView(ViewBase):
    """
    Basic view for starting/replying/editing
    """
    template = 'misago/posting/formset.html'

    def find_mode(self, request, *args, **kwargs):
        """
        First step: guess from request what kind of view we are
        """
        is_submit = request.method == 'POST' and 'submit' in request.POST
        if is_submit:
            request.user.lock()

        forum = self.get_forum(request, lock=is_submit, **kwargs)

        thread = None
        post = None

        if 'thread_id' in kwargs:
            thread = self.get_thread(
                request, lock=is_submit, queryset=forum.thread_set, **kwargs)

        if thread:
            mode = REPLY
        else:
            mode = START
            thread = Thread(forum=forum)

        if not post:
            post = Post(forum=forum, thread=thread)

        return mode, forum, thread, post

    def allow_mode(self, user, mode, forum, thread, post):
        """
        Second step: check start/reply/edit permissions
        """
        if mode == START:
            self.allow_start(user, forum)
        if mode == REPLY:
            self.allow_reply(user, forum, thread)
        if mode == EDIT:
            self.allow_edit(user, forum, thread, post)

    def allow_start(self, user, forum):
        allow_start_thread(user, forum)

    def allow_reply(self, user, forum, thread):
        allow_reply_thread(user, thread)

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
        mode, forum, thread, post = mode_context

        if not request.is_ajax():
            response = render(request, 'misago/errorpages/wrong_way.html')
            response.status_code = 405
            return response

        forum.labels = Label.objects.get_forum_labels(forum)
        formset = EditorFormset(request=request,
                                mode=mode,
                                user=request.user,
                                forum=forum,
                                thread=thread,
                                post=post)

        if request.method == 'POST':
            if 'submit' in request.POST:
                if formset.is_valid():
                    try:
                        formset.save()

                        if mode == START:
                            message = _("New thread was posted.")
                        if mode == REPLY:
                            message = _("Your reply was posted.")
                        if mode == EDIT:
                            message = _("Message was edited.")
                        messages.success(request, message)

                        return JsonResponse({
                            'post_url': goto.post(request.user, thread, post)
                        })
                    except PostingInterrupt as e:
                        return JsonResponse({'interrupt': e.message})
                else:
                    return JsonResponse({'errors': formset.errors})

            if 'preview' in request.POST:
                formset.update()
                return JsonResponse({'preview': formset.post.parsed})

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
            'api_url': request.path
        })
