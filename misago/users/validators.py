import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email as validate_email_content
from django.utils.translation import ungettext, ugettext_lazy as _
from django.contrib.auth import get_user_model
from misago.conf import settings


ALPHANUMERICS_RE = re.compile('[\W_]+', re.UNICODE)
USERNAME_RE = re.compile(r'^[0-9a-z]+$', re.IGNORECASE)


def validate_email_available(value):
    User = get_user_model()

    try:
        User.objects.get_by_email(value)
    except User.DoesNotExist:
        pass
    else:
        raise ValidationError(_("This e-mail address is not available."))


def validate_email_banned(value):
    """TODO for when bans will be reimplemented from 0.5"""


def validate_email(value):
    """shortcut function that does complete validation of email"""
    validate_email_content(value)
    validate_email_available(value)
    validate_email_banned(value)


def _validate_password_alphanumerics(value):
    digits_len = len(filter(type(value).isdigit, value))

    if not digits_len or digits_len == len(value):
        raise ValidationError(
            _("Password must contain digits in addition to other characters."))


def _validate_password_case(value):
    for char in value:
        if char != char.lower():
            break
    else:
        raise ValidationError(
            _("Password must contain characters with different cases."))



def _validate_password_special(value):
    alphanumerics_len = len(ALPHANUMERICS_RE.sub('', value))

    if not alphanumerics_len or alphanumerics_len == len(value):
        raise ValidationError(
            _("Password must contain special signs "
              "in addition to other characters."))


PASSWORD_COMPLEXITY_RULES = {
    'alphanumerics': _validate_password_alphanumerics,
    'case': _validate_password_case,
    'special': _validate_password_special,
}


def validate_password_complexity(value):
    for test in settings.password_complexity:
        PASSWORD_COMPLEXITY_RULES[test](value)


def validate_password_length(value):
    if len(value) < settings.password_length_min:
        message = ungettext(
            'Valid password must be at least one character long.',
            'valid password must be at least %(length)d characters long.',
            settings.password_length_min)
        message = message % {'length': settings.password_length_min}
        raise ValidationError(message)


def validate_password(value):
    """shortcut function that does complete validation of password"""
    validate_password_length(value)
    validate_password_complexity(value)


def validate_username_available(value):
    User = get_user_model()

    try:
        User.objects.get_by_username(value)
    except User.DoesNotExist:
        pass
    else:
        raise ValidationError(_("This username is not available."))


def validate_username_banned(value):
    """TODO for when bans will be reimplemented from 0.5"""


def validate_username_content(value):
    if not USERNAME_RE.match(value):
        raise ValidationError(
            _("Username can only contain latin alphabet letters and digits."))


def validate_username_length(value):
    if len(value) < settings.username_length_min:
        message = ungettext(
            'Username must be at least one character long.',
            'Username must be at least %(length)d characters long.',
            settings.username_length_min)
        message = message % {'length': settings.username_length_min}
        raise ValidationError(message)

    if len(value) > settings.username_length_max:
        message = ungettext(
            "Username cannot be longer than one characters.",
            "Username cannot be longer than %(length)d characters.",
            settings.username_length_max)
        message = message % {'length': settings.username_length_max}
        raise ValidationError(message)


def validate_username(value):
    """shortcut function that does complete validation of username"""
    validate_username_content(value)
    validate_username_length(value)
    validate_username_available(value)
    validate_username_banned(value)
