from django.utils.translation import ugettext_lazy as _, ungettext

from misago.conf import settings
from misago.core import forms
from misago.core.validators import validate_sluggable
from misago.markup import common_flavour


class ReplyForm(forms.Form):
    is_main = True
    legend = _("Reply")
    template = "misago/posting/replyform.html"
    js_template = "misago/posting/replyform_js.html"

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

        self.post_instance.original = self.parsing_result['original_text']
        self.post_instance.parsed = self.parsing_result['parsed_text']

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


class ThreadPrefixFormBase(forms.Form):
    is_supporting = True
    legend = _("Prefix")
    template = "misago/posting/threadprefixform.html"

    prefix = forms.TypedChoiceField(label=_("Thread weight"), initial=0,
                                    choices=(
                                        (0, _("Standard")),
                                        (1, _("Pinned")),
                                        (2, _("Announcement")),
                                    ))


def ThreadPrefixForm(*args, **kwargs):
    return ThreadPrefixFormBase(*args, **kwargs)


class ThreadWeightForm(forms.Form):
    is_supporting = True
    legend = _("Weight")
    template = "misago/posting/threadweightform.html"

    weight = forms.TypedChoiceField(label=_("Thread weight"), initial=0,
                                    choices=(
                                        (0, _("Standard")),
                                        (1, _("Pinned")),
                                        (2, _("Announcement")),
                                    ))


class ThreadCloseForm(forms.Form):
    is_supporting = True
    legend = _("Close thread")
    template = "misago/posting/threadcloseform.html"

    is_closed = forms.YesNoSwitch(label=_("Close thread"), initial=0)
