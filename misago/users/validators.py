import json
import re

import requests

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email as validate_email_content
from django.utils.encoding import force_str
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

from misago.conf import settings

from .bans import get_email_ban, get_username_ban


USERNAME_RE = re.compile(r'^[0-9a-z]+$', re.IGNORECASE)

UserModel = get_user_model()


# E-mail validators
def validate_email_available(value, exclude=None):
    try:
        user = UserModel.objects.get_by_email(value)
        if not exclude or user.pk != exclude.pk:
            raise ValidationError(_("This e-mail address is not available."))
    except UserModel.DoesNotExist:
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


# Username validators
def validate_username_available(value, exclude=None):
    try:
        user = UserModel.objects.get_by_username(value)
        if not exclude or user.pk != exclude.pk:
            raise ValidationError(_("This username is not available."))
    except UserModel.DoesNotExist:
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
        raise ValidationError(_("Username can only contain latin alphabet letters and digits."))


def validate_username_length(value):
    if len(value) < settings.username_length_min:
        message = ungettext(
            "Username must be at least %(limit_value)s character long.",
            "Username must be at least %(limit_value)s characters long.",
            settings.username_length_min
        )
        raise ValidationError(message % {'limit_value': settings.username_length_min})

    if len(value) > settings.username_length_max:
        message = ungettext(
            "Username cannot be longer than %(limit_value)s characters.",
            "Username cannot be longer than %(limit_value)s characters.",
            settings.username_length_max
        )
        raise ValidationError(message % {'limit_value': settings.username_length_max})


def validate_username(value, exclude=None):
    """shortcut function that does complete validation of username"""
    validate_username_length(value)
    validate_username_content(value)
    validate_username_available(value, exclude)
    validate_username_banned(value)


# New account validators
SFS_API_URL = u'http://api.stopforumspam.org/api?email=%(email)s&ip=%(ip)s&f=json&confidence'  # noqa


def validate_with_sfs(request, form, cleaned_data):
    if settings.MISAGO_USE_STOP_FORUM_SPAM and cleaned_data.get('email'):
        _real_validate_with_sfs(request.user_ip, cleaned_data['email'])


def _real_validate_with_sfs(ip, email):
    try:
        r = requests.get(SFS_API_URL % {'email': email, 'ip': ip}, timeout=5)

        r.raise_for_status()

        api_response = json.loads(force_str(r.content))
        ip_score = api_response.get('ip', {}).get('confidence', 0)
        email_score = api_response.get('email', {}).get('confidence', 0)

        api_score = max((ip_score, email_score))

        if api_score > settings.MISAGO_STOP_FORUM_SPAM_MIN_CONFIDENCE:
            raise ValidationError(_("Data entered was found in spammers database."))
    except requests.exceptions.RequestException:
        pass  # todo: log those somewhere


def validate_gmail_email(request, form, cleaned_data):
    email = cleaned_data.get('email', '')
    if '@' not in email:
        return

    username, domain = email.lower().split('@')
    if domain == 'gmail.com' and username.count('.') > 5:
        form.add_error('email', ValidationError(_("This email is not allowed.")))


# Registration validation
validators_list = settings.MISAGO_NEW_REGISTRATIONS_VALIDATORS
REGISTRATION_VALIDATORS = list(map(import_string, validators_list))


def validate_new_registration(request, form, cleaned_data, validators=None):
    validators = validators or REGISTRATION_VALIDATORS

    for validator in validators:
        validator(request, form, cleaned_data)
