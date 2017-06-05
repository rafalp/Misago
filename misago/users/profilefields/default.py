from django.utils.translation import ugettext_lazy as _

from . import TextProfileField, TextareaProfileField


class BioField(TextareaProfileField):
    fieldname = 'bio'
    label = _("Bio")


class FullNameField(TextProfileField):
    fieldname = 'fullname'
    label = _("Full name")


class LocationField(TextProfileField):
    fieldname = 'location'
    label = _("Location")
