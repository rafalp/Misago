from django import forms
from django.utils.translation import ungettext
from misago.utils.strings import slugify

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
