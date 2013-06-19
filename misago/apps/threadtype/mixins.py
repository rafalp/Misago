from django import forms
from django.utils import timezone
from django.utils.translation import ungettext, ugettext_lazy as _
from misago.utils.strings import slugify

class FloodProtectionMixin(object):
    def clean(self):
        cleaned_data = super(FloodProtectionMixin, self).clean()
        diff = timezone.now() - self.request.user.last_post
        diff = diff.seconds + (diff.days * 86400)
        if diff < 35:
            raise forms.ValidationError(_("You can't post one message so quickly after another. Please wait a moment and try again."))
        return cleaned_data


class ValidateThreadNameMixin(object):
    def clean_thread_name(self):
        data = self.cleaned_data['thread_name']
        slug = slugify(data)
        if len(slug) < self.request.settings['thread_name_min']:
            raise forms.ValidationError(ungettext(
                                                  "Thread name must contain at least one alpha-numeric character.",
                                                  "Thread name must contain at least %(count)d alpha-numeric characters.",
                                                  self.request.settings['thread_name_min']
                                                  ) % {'count': self.request.settings['thread_name_min']})
        if len(data) > self.request.settings['thread_name_max']:
            raise forms.ValidationError(ungettext(
                                                  "Thread name cannot be longer than %(count)d character.",
                                                  "Thread name cannot be longer than %(count)d characters.",
                                                  self.request.settings['thread_name_max']
                                                  ) % {'count': self.request.settings['thread_name_max']})
        return data


class ValidatePostLengthMixin(object):
    def clean_post(self):
        data = self.cleaned_data['post']
        if len(data) < self.request.settings['post_length_min']:
            raise forms.ValidationError(ungettext(
                                                  "Post content cannot be empty.",
                                                  "Post content cannot be shorter than %(count)d characters.",
                                                  self.request.settings['post_length_min']
                                                  ) % {'count': self.request.settings['post_length_min']})
        return data