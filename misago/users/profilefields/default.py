from __future__ import unicode_literals

import re

from django.forms import ValidationError
from django.utils.translation import ugettext, ugettext_lazy as _

from . import basefields


class BioField(basefields.UrlifiedTextareaProfileField):
    fieldname = 'bio'
    label = _("Bio")


class FullNameField(basefields.TextProfileField):
    fieldname = 'fullname'
    label = _("Full name")


class LocationField(basefields.TextProfileField):
    fieldname = 'location'
    label = _("Location")


class GenderField(basefields.ChoiceProfileField):
    fieldname = 'gender'
    label = _("Gender")

    choices = (
        ('', _('Not specified')),
        ('secret', _('Not telling')),
        ('female', _('Female')),
        ('male', _('Male')),
    )


class WebsiteField(basefields.UrlProfileField):
    fieldname = 'website'
    label = _("Website")


class SkypeHandleField(basefields.TextProfileField):
    fieldname = 'skype'
    label = _("Skype ID")


class TwitterHandleField(basefields.TextProfileField):
    fieldname = 'twitter'
    label = _("Twitter handle")
    help_text = _('Without leading "@" sign.')

    def get_value_display_data(self, request, user, data):
        return {
            'text': '@{}'.format(data),
            'url': 'https://twitter.com/{}'.format(data),
        }

    def clean(self, request, user, data):
        data = data.lstrip('@')
        if data and not re.search('^[A-Za-z0-9_]+$', data):
            raise ValidationError(ugettext("This is not a valid twitter handle."))
        return data
