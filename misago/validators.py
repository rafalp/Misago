import re
from django.core.exceptions import ValidationError
from django.utils.translation import ungettext, ugettext_lazy as _
from misago.conf import settings
from misago.models import Ban
from misago.utils.strings import slugify

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


def validate_username(value):
    value = unicode(value).strip()

    if len(value) < settings.username_length_min:
        raise ValidationError(ungettext(
            'Username must be at least one character long.',
            'Username must be at least %(count)d characters long.',
            settings.username_length_min
        ) % {
            'count': settings.username_length_min,
        })

    if len(value) > settings.username_length_max:
        raise ValidationError(ungettext(
            'Username cannot be longer than one characters.',
            'Username cannot be longer than %(count)d characters.',
            settings.username_length_max
        ) % {
            'count': settings.username_length_max,
        })

    if settings.UNICODE_USERNAMES:
        if not re.search('^[^\W_]+$', value, re.UNICODE):
            raise ValidationError(_("Username can only contain letters and digits."))
    else:
        if not re.search('^[^\W_]+$', value):
            raise ValidationError(_("Username can only contain latin alphabet letters and digits."))
    
    if Ban.objects.check_ban(username=value):
        raise ValidationError(_("This username is forbidden."))


def validate_password(value):
    value = unicode(value).strip()

    if len(value) < settings.password_length:
        raise ValidationError(ungettext(
            'Correct password has to be at least one character long.',
            'Correct password has to be at least %(count)d characters long.',
            settings.password_length
        ) % {
            'count': settings.password_length,
        })

    for test in settings.password_complexity:
        if test in ('case', 'digits', 'special'):
            if not re.search('[a-zA-Z]', value):
                raise ValidationError(_("Password must contain alphabetical characters."))
            if test == 'case':
                if not (re.search('[a-z]', value) and re.search('[A-Z]', value)):
                    raise ValidationError(_("Password must contain characters that have different case."))
            if test == 'digits':
                if not re.search('[0-9]', value):
                    raise ValidationError(_("Password must contain digits in addition to characters."))
            if test == 'special':
                if not re.search('[^0-9a-zA-Z]', value):
                    raise ValidationError(_("Password must contain special (non alphanumerical) characters."))


def validate_email(value):
    value = unicode(value).strip()
    if Ban.objects.check_ban(email=value):
        raise ValidationError(_("This board forbids registrations using this e-mail address."))
