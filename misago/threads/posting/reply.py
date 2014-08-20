from django.db.models import F

from misago.markup import Editor

from misago.threads.checksums import update_post_checksum
from misago.threads.forms.reply import (ReplyForm, ThreadForm,
                                        PrefixedThreadForm)
from misago.threads.posting import EditorFormsetMiddleware, START, REPLY, EDIT


class ReplyFormMiddleware(EditorFormsetMiddleware):
    def make_form(self):
        initial_data = {'title': self.thread.title, 'post': self.post.post}

        if self.mode == START:
            if self.request.method == 'POST':
                form = ThreadForm(self.thread, self.post, self.request.POST)
            else:
                form = ThreadForm(self.thread, self.post, initial=initial_data)
        else:
            if self.request.method == 'POST':
                form = ReplyForm(self.post, self.request.POST)
            else:
                form = ReplyForm(self.post, initial=initial_data)

        form.post_editor = Editor(form['post'])
        return form

    def pre_save(self, form):
        self.parsing_result.update(form.parsing_result)

    def save(self, form):
        # if we are starting new thread, create empty model
        if self.mode == START:
            self.thread.set_title(form.cleaned_data['title'])
            self.thread.starter_name = '-'
            self.thread.starter_slug = '-'
            self.thread.last_poster_name = '-'
            self.thread.last_poster_slug = '-'
            self.thread.started_on = self.datetime
            self.thread.last_post_on = self.datetime
            self.thread.save()

        # make changes/set data on post
        self.post.updated_on = self.datetime
        if self.mode == EDIT:
            self.post.last_editor_name = self.user
            self.post.poster_name = self.user.username
            self.post.poster_slug = self.user.slug
        else:
            self.post.thread = self.thread
            self.post.poster = self.user
            self.post.poster_name = self.user.username
            self.post.poster_ip = self.request._misago_real_ip
            self.post.posted_on = self.datetime

        self.post.post_checksum = update_post_checksum(self.post)
        self.post.save()

        # Update thread
        if self.mode == START:
            self.forum.threads += 1
            self.thread.set_first_post(self.post)

        if self.mode != EDIT:
            self.thread.set_last_post(self.post)
        if self.mode != REPLY:
            self.thread.replies += 1
        self.thread.save()

        # update forum
        if self.mode != EDIT:
            self.forum.set_last_thread(self.thread)
            self.forum.posts += 1
            self.forum.save()

        # update poster
        if self.mode == START:
            self.user.threads = F('threads') + 1

        if self.mode != EDIT:
            self.user.posts = F('posts') + 1
        self.user.save(update_fields=['threads', 'posts'])
