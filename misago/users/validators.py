import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email as validate_email_content
from django.utils.translation import ungettext, ugettext_lazy as _
from django.contrib.auth import get_user_model
from misago.conf import settings


USERNAME_RE = re.compile(r'^[0-9a-z]+$', re.IGNORECASE)


"""
Email validators
"""
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


"""
Password validators
"""
def validate_password(value):
    if len(value) < settings.password_length_min:
        message = ungettext(
            'Valid password must be at least one character long.',
            'Valid password must be at least %(length)d characters long.',
            settings.password_length_min)
        message = message % {'length': settings.password_length_min}
        raise ValidationError(message)


"""
Username validators
"""
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
