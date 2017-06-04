from django.utils.translation import ugettext_lazy as _

from . import TextProfileField


class FullNameField(TextProfileField):
    fieldname = 'fullname'
    label = _("Full name")
