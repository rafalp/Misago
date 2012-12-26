from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from misago.utils import slugify

class validate_sluggable(object):
    def __init__(self, error_short=None, error_long=None):
        self.error_short = error_short if error_short else _("Value has to contain alpha-numerical characters.")
        self.error_long = error_long if error_long else _("Value is too long.")
         
    def __call__(self, value):
        slug = slugify(value)
        if not slug:
            raise ValidationError(self.error_short)
        if len(slug) > 255:
            raise ValidationError(self.error_long)