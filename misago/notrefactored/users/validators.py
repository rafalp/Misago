import re
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ungettext, ugettext_lazy as _
from misago.banning.models import check_ban
from misago.settings.settings import Settings as DBSettings

def validate_username(value, db_settings):
    value = unicode(value).strip()
    if len(value) < db_settings['username_length_min']:
        raise ValidationError(ungettext(
            'Username must be at least one character long.',
            'Username must be at least %(count)d characters long.',
            db_settings['username_length_min']
        ) % {
            'count': db_settings['username_length_min'],
        })
    if len(value) > db_settings['username_length_max']:
        raise ValidationError(ungettext(
            'Username cannot be longer than one characters.',
            'Username cannot be longer than %(count)d characters.',
            db_settings['username_length_max']
        ) % {
            'count': db_settings['username_length_max'],
        })
    if settings.UNICODE_USERNAMES:
        if not re.search('^[^\W_]+$', value, re.UNICODE):
            raise ValidationError(_("Username can only contain letters and digits."))
    else:
        if not re.search('^[^\W_]+$', value):
            raise ValidationError(_("Username can only contain latin alphabet letters and digits."))
    if check_ban(username=value):
        raise ValidationError(_("This username is forbidden."))


def validate_password(value, db_settings):
    value = unicode(value).strip()
    if len(value) < db_settings['password_length']:
        raise ValidationError(ungettext(
            'Correct password has to be at least one character long.',
            'Correct password has to be at least %(count)d characters long.',
            db_settings['password_length']
        ) % {
            'count': db_settings['password_length'],
        })
    for test in db_settings['password_complexity']:
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
    if check_ban(email=value):
        raise ValidationError(_("This board forbids registrations using this e-mail address."))
