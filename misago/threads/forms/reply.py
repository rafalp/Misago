from django.db.models import F
from django.utils.translation import ugettext_lazy as _, ungettext

from misago.conf import settings
from misago.core import forms
from misago.core.validators import validate_sluggable
from misago.markup import Editor, common_flavour

from misago.threads.checksums import update_post_checksum
from misago.threads.forms.posting import (EditorFormsetMiddleware,
                                          START, REPLY, EDIT)


class ReplyForm(forms.Form):
    is_main = True
    legend = _("Reply")
    template = "misago/threads/replyform.html"
    js_template = "misago/threads/replyform_js.html"

    post = forms.CharField(label=_("Message body"), required=False)

    def __init__(self, post=None, *args, **kwargs):
        self.post_instance = post
        self.parsing_result = {}

        super(ReplyForm, self).__init__(*args, **kwargs)

    def validate_post(self, post):
        post_len = len(post)
        if not post_len:
            raise forms.ValidationError(_("Enter message."))

        if post_len < settings.post_length_min:
            message = ungettext(
                "Posted message should be at least %(limit)s character long.",
                "Posted message should be at least %(limit)s characters long.",
                settings.post_length_min)
            message = message % {'limit': settings.post_length_min}
            raise forms.ValidationError(message)

        if settings.post_length_max and post_len > settings.post_length_max:
            message = ungettext(
                "Posted message can't be longer than %(limit)s character.",
                "Posted message can't be longer than %(limit)s characters.",
                settings.post_length_max,)
            message = message % {'limit': settings.post_length_max}
            raise forms.ValidationError(message)

        self.parsing_result = common_flavour(post, self.post_instance.poster)

        self.post_instance.post = self.parsing_result['original_text']
        self.post_instance.post_parsed = self.parsing_result['parsed_text']

    def validate_data(self, data):
        self.validate_post(data.get('post', ''))

    def clean(self):
        data = super(ReplyForm, self).clean()
        self.validate_data(data)
        return data


class ThreadForm(ReplyForm):
    legend = _("Thread ")

    title = forms.CharField(label=_("Thread title"), required=False)

    def __init__(self, thread=None, *args, **kwargs):
        self.thread_instance = thread
        super(ThreadForm, self).__init__(*args, **kwargs)

    def validate_title(self, title):
        title_len = len(title)

        if not title_len:
            raise forms.ValidationError(_("Enter thread title."))

        if title_len < settings.thread_title_length_min:
            message = ungettext(
                "Thread title should be at least %(limit)s character long.",
                "Thread title should be at least %(limit)s characters long.",
                settings.thread_title_length_min)
            message = message % {'limit': settings.thread_title_length_min}
            raise forms.ValidationError(message)

        if title_len > settings.thread_title_length_max:
            message = ungettext(
                "Thread title can't be longer than %(limit)s character.",
                "Thread title can't be longer than %(limit)s characters.",
                settings.thread_title_length_max,)
            message = message % {'limit': settings.thread_title_length_max}
            raise forms.ValidationError(message)

        error_not_sluggable = _("Thread title should contain "
                                "alpha-numeric characters.")
        error_slug_too_long = _("Thread title is too long.")
        slug_validator = validate_sluggable(error_not_sluggable,
                                            error_slug_too_long)
        slug_validator(title)

    def validate_data(self, data):
        errors = []

        if not data.get('title') and not data.get('post'):
            raise forms.ValidationError(_("Enter thread title and message."))

        try:
            self.validate_title(data.get('title', ''))
        except forms.ValidationError as e:
            errors.append(e)

        try:
            self.validate_post(data.get('post', ''))
        except forms.ValidationError as e:
            errors.append(e)

        if errors:
            raise forms.ValidationError(errors)


class PrefixedThreadForm(ThreadForm):
    pass


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
