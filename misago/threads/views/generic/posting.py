from django.contrib import messages
from django.db.transaction import atomic
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import html
from django.utils.translation import ugettext as _
from django.views.generic import View

from misago.categories.lists import get_category_path
from misago.core.errorpages import not_allowed
from misago.core.exceptions import AjaxError

from misago.threads import goto
from misago.threads.posting import (PostingInterrupt, EditorFormset,
                                    START, REPLY, EDIT)
from misago.threads.models import Thread, Post, Label
from misago.threads.permissions import (allow_start_thread, allow_reply_thread,
                                        allow_edit_post)
from misago.threads.views.generic.base import ViewBase


__all__ = ['PostingView']


class PostingView(ViewBase):
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

        category = None
        thread = None
        post = None

        if 'post_id' in kwargs:
            post = self.get_post(request, lock=is_submit, **kwargs)
            category = post.category
            thread = post.thread
        elif 'thread_id' in kwargs:
            thread = self.get_thread(request, lock=is_submit, **kwargs)
            category = thread.category
        else:
            category = self.get_category(request, lock=is_submit, **kwargs)

        if thread:
            if post:
                mode = EDIT
            else:
                mode = REPLY
        else:
            mode = START
            thread = Thread(category=category)

        if not post:
            post = Post(category=category, thread=thread)

        return mode, category, thread, post

    def allow_mode(self, user, mode, category, thread, post):
        """
        Second step: check start/reply/edit permissions
        """
        if mode == START:
            self.allow_start(user, category)
        if mode == REPLY:
            self.allow_reply(user, thread)
        if mode == EDIT:
            self.allow_edit(user, post)

    def allow_start(self, user, category):
        allow_start_thread(user, category)

    def allow_reply(self, user, thread):
        allow_reply_thread(user, thread)

    def allow_edit(self, user, post):
        allow_edit_post(user, post)

    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            return not_allowed(request)

        if request.method == 'POST':
            with atomic():
                return self.real_dispatch(request, *args, **kwargs)
        else:
            return self.real_dispatch(request, *args, **kwargs)

    def real_dispatch(self, request, *args, **kwargs):
        mode_context = self.find_mode(request, *args, **kwargs)
        self.allow_mode(request.user, *mode_context)
        mode, category, thread, post = mode_context

        category.labels = Label.objects.get_category_labels(category)
        formset = EditorFormset(request=request,
                                mode=mode,
                                user=request.user,
                                category=category,
                                thread=thread,
                                post=post)

        if request.method == 'POST':
            if 'submit' in request.POST:
                if formset.is_valid():
                    try:
                        formset.save()
                        return self.handle_submit(request, formset)
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
            'category': category,
            'path': get_category_path(category),
            'thread': thread,
            'post': post,
            'api_url': request.path
        })

    def handle_submit(self, request, formset):
        mode, category, thread, post = (formset.mode, formset.category,
                                     formset.thread, formset.post)
        if mode == EDIT:
            message = _("Changes saved.")
        else:
            if mode == START:
                message = _("New thread was posted.")
            if mode == REPLY:
                message = _("Your reply was posted.")
            messages.success(request, message)

        posts_qs = self.exclude_invisible_posts(thread.post_set,
                                                request.user,
                                                category,
                                                thread)
        post_url = goto.post(thread, posts_qs, post)

        return JsonResponse({
            'message': message,
            'post_url': post_url,
            'parsed': post.parsed,
            'original': post.original,
            'title': thread.title,
            'title_escaped': html.escape(thread.title),
        })
