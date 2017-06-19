from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

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

    def get_display_data(self, request, user, data):
        return {
            'text': '@{}'.format(data),
            'url': 'https://twitter.com/{}'.format(data),
        }

    def clean_field(self, request, user, data):
        return data.lstrip('@').replace('/', '').replace('\\', '')
