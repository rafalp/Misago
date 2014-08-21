from misago.markup import Editor

from misago.threads.checksums import update_post_checksum
from misago.threads.forms.reply import (ReplyForm, ThreadForm,
                                        PrefixedThreadForm)
from misago.threads.posting import PostingMiddleware, START, REPLY, EDIT


class ReplyFormMiddleware(PostingMiddleware):
    def make_form(self):
        initial_data = {'title': self.thread.title, 'post': self.post.original}

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
        if self.mode == START:
            self.new_thread(form)

        if self.mode == EDIT:
            self.edit_post()
        else:
            self.new_post()

        self.post.updated_on = self.datetime
        self.post.post_checksum = update_post_checksum(self.post)
        self.post.save()

    def new_thread(self, form):
        self.thread.set_title(form.cleaned_data['title'])
        self.thread.starter_name = self.user.username
        self.thread.starter_slug = self.user.slug
        self.thread.last_poster_name = self.user.username
        self.thread.last_poster_slug = self.user.slug
        self.thread.started_on = self.datetime
        self.thread.last_post_on = self.datetime
        self.thread.save()

    def edit_post(self):
        self.post.last_editor_name = self.user
        self.post.poster_name = self.user.username
        self.post.poster_slug = self.user.slug

    def new_post(self):
        self.post.thread = self.thread
        self.post.poster = self.user
        self.post.poster_name = self.user.username
        self.post.poster_ip = self.request._misago_real_ip
        self.post.posted_on = self.datetime

