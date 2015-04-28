from misago.markup import Editor

from misago.threads.checksums import update_post_checksum
from misago.threads.forms.posting import ReplyForm, ThreadForm
from misago.threads.permissions import can_edit_thread
from misago.threads.posting import PostingMiddleware, START, REPLY, EDIT


class ReplyFormMiddleware(PostingMiddleware):
    def make_form(self):
        initial_data = {'title': self.thread.title, 'post': self.post.original}

        if self.mode == EDIT:
            is_first_post = self.post.id == self.thread.first_post_id
            if is_first_post and can_edit_thread(self.user, self.thread):
                FormType = ThreadForm
            else:
                FormType = ReplyForm
        elif self.mode == START:
            FormType = ThreadForm
        else:
            FormType = ReplyForm

        if FormType == ThreadForm:
            if self.request.method == 'POST':
                form = FormType(
                    self.thread, self.post, self.request, self.request.POST)
            else:
                form = FormType(
                    self.thread, self.post, self.request, initial=initial_data)
        else:
            if self.request.method == 'POST':
                form = FormType(
                    self.post, self.request, self.request.POST)
            else:
                form = FormType(
                    self.post, self.request, initial=initial_data)

        form.post_editor = Editor(form['post'], has_preview=True)
        return form

    def pre_save(self, form):
        if form.is_valid():
            self.parsing_result.update(form.parsing_result)

    def save(self, form):
        if self.mode == START:
            self.new_thread(form)

        if self.mode == EDIT:
            self.edit_post(form)
        else:
            self.new_post()

        self.post.updated_on = self.datetime
        self.post.save()

        update_post_checksum(self.post)
        self.post.update_fields.append('checksum')

    def new_thread(self, form):
        self.thread.set_title(form.cleaned_data['title'])
        self.thread.starter_name = self.user.username
        self.thread.starter_slug = self.user.slug
        self.thread.last_poster_name = self.user.username
        self.thread.last_poster_slug = self.user.slug
        self.thread.started_on = self.datetime
        self.thread.last_post_on = self.datetime
        self.thread.save()

    def edit_post(self, form):
        if form.cleaned_data.get('title'):
            self.thread.set_title(form.cleaned_data['title'])
            self.thread.update_fields.extend(('title', 'slug'))

    def new_post(self):
        self.post.thread = self.thread
        self.post.poster = self.user
        self.post.poster_name = self.user.username
        self.post.poster_ip = self.request.user_ip
        self.post.posted_on = self.datetime
