import re
from django.core.exceptions import ValidationError
from django.utils.translation import ungettext, ugettext_lazy as _
from django.contrib.auth import get_user_model
from misago.conf import settings


USERNAME_REGEX = re.compile(r'^[0-9a-z]+$', re.IGNORECASE)


def validate_username_available(value):
    User = get_user_model()

    try:
        User.objects.get_by_username(value)
    except User.DoesNotExist:
        pass
    else:
        raise ValidationError(_("This username is not available."))


def validate_username_content(value):
    if not USERNAME_REGEX.match(value):
        raise ValidationError(
            _("Username can only contain latin alphabet letters and digits."))


def validate_username_length(value):
    if len(value) < settings.username_length_min:
        message = ungettext(
            'Username must be at least one character long.',
            'Username must be at least %(count)d characters long.',
            settings.username_length_min)
        message = message % {'count': settings.username_length_min}
        raise ValidationError(message)

    if len(value) > settings.username_length_max:
        message = ungettext(
            "Username cannot be longer than one characters.",
            "Username cannot be longer than %(count)d characters.",
            settings.username_length_max)
        message = message % {'count': settings.username_length_max}
        raise ValidationError(message)


def validate_username(value):
    """Shortcut function that does complete validation of username"""
    validate_username_content(value)
    validate_username_length(value)
    validate_username_available(value)


def validate_email_available(value):
    User = get_user_model()

    try:
        User.objects.get_by_email(value)
    except User.DoesNotExist:
        pass
    else:
        raise ValidationError(_("This e-mail address is not available."))
