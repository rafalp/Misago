from importlib import import_module
import json
import re

import requests

from django.core.exceptions import PermissionDenied, ValidationError
from django.core.validators import validate_email as validate_email_content
from django.utils.translation import ungettext, ugettext_lazy as _
from django.contrib.auth import get_user_model

from misago.conf import settings

from misago.users.bans import get_email_ban, get_username_ban


USERNAME_RE = re.compile(r'^[0-9a-z]+$', re.IGNORECASE)


"""
Email validators
"""
def validate_email_available(value, exclude=None):
    User = get_user_model()
    try:
        user = User.objects.get_by_email(value)
        if not exclude or user.pk != exclude.pk:
            raise ValidationError(_("This e-mail address is not available."))
    except User.DoesNotExist:
        pass


def validate_email_banned(value):
    ban = get_email_ban(value)

    if ban:
        if ban.user_message:
            raise ValidationError(ban.user_message)
        else:
            raise ValidationError(_("This e-mail address is not allowed."))


def validate_email(value, exclude=None):
    """shortcut function that does complete validation of email"""
    validate_email_content(value)
    validate_email_available(value, exclude)
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
def validate_username_available(value, exclude=None):
    User = get_user_model()
    try:
        user = User.objects.get_by_username(value)
        if not exclude or user.pk != exclude.pk:
            raise ValidationError(_("This username is not available."))
    except User.DoesNotExist:
        pass


def validate_username_banned(value):
    ban = get_username_ban(value)

    if ban:
        if ban.user_message:
            raise ValidationError(ban.user_message)
        else:
            raise ValidationError(_("This username is not allowed."))


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


def validate_username(value, exclude=None):
    """shortcut function that does complete validation of username"""
    validate_username_length(value)
    validate_username_content(value)
    validate_username_available(value, exclude)
    validate_username_banned(value)


"""
New account validators
"""
SFS_API_URL = 'http://api.stopforumspam.org/api?email=%(email)s&ip=%(ip)s&f=json&confidence'  # noqa


def validate_with_sfs(ip, username, email):
    if settings.MISAGO_STOP_FORUM_SPAM_USE:
        _real_validate_with_sfs(ip, email)


def _real_validate_with_sfs(ip, email):
    try:
        r = requests.get(SFS_API_URL % {'email': email, 'ip': ip},
                         timeout=3)
        api_response = json.loads(r.content)
        ip_score = api_response.get('ip', {}).get('confidence', 0)
        email_score = api_response.get('email', {}).get('confidence', 0)

        api_score = max((ip_score, email_score))

        if api_score > settings.MISAGO_STOP_FORUM_SPAM_MIN_CONFIDENCE:
            raise PermissionDenied()
    except requests.exceptions.RequestException:
        pass # todo: log those somewhere


"""
Registration validation
"""
REGISTRATION_VALIDATORS = []


def load_registration_validators():
    for path in settings.MISAGO_NEW_REGISTRATIONS_VALIDATORS:
        module = import_module('.'.join(path.split('.')[:-1]))
        REGISTRATION_VALIDATORS.append(getattr(module, path.split('.')[-1]))


if settings.MISAGO_NEW_REGISTRATIONS_VALIDATORS:
    load_registration_validators()


def validate_new_registration(ip, username, email, validators=None):
    validators = validators or REGISTRATION_VALIDATORS

    for validator in validators:
        validator(ip, username, email)
