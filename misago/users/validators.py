import json
import logging
import re

import requests
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.encoding import force_str
from django.utils.module_loading import import_string
from django.utils.translation import npgettext, pgettext_lazy
from requests.exceptions import RequestException

from .. import hooks
from ..conf import settings
from .bans import get_email_ban, get_username_ban

USERNAME_RE = re.compile(r"^[0-9a-z_]+$", re.IGNORECASE)
USERNAME_LATIN_ALPHA_RE = re.compile(r"[0-9a-z]", re.IGNORECASE)

logger = logging.getLogger("misago.users.validators")

User = get_user_model()


# E-mail validators
dj_validate_email = EmailValidator(
    message=pgettext_lazy("email validator", "Enter a valid e-mail address.")
)


def validate_email(value, exclude=None):
    """shortcut function that does complete validation of email"""
    dj_validate_email(value)
    validate_email_available(value, exclude)
    validate_email_banned(value)


def validate_email_available(value, exclude=None):
    try:
        user = User.objects.get_by_email(value)
        if not exclude or user.pk != exclude.pk:
            raise ValidationError(
                pgettext_lazy(
                    "user email validator", "This e-mail address is not available."
                )
            )
    except User.DoesNotExist:
        pass


def validate_email_banned(value):
    ban = get_email_ban(value, registration_only=True)

    if ban:
        if ban.user_message:
            raise ValidationError(ban.user_message)
        else:
            raise ValidationError(
                pgettext_lazy(
                    "user email validator", "This e-mail address is not allowed."
                )
            )


# Username validators
def validate_username(settings, value, exclude=None):
    """shortcut function that does complete validation of username"""
    validate_username_length(settings, value)
    validate_username_content(value)
    validate_username_available(value, exclude)
    validate_username_banned(value)


def validate_username_available(value, exclude=None):
    try:
        user = User.objects.get_by_username(value)
        if not exclude or user.pk != exclude.pk:
            raise ValidationError(
                pgettext_lazy("username validator", "This username is not available.")
            )
    except User.DoesNotExist:
        pass


def validate_username_banned(value):
    ban = get_username_ban(value, registration_only=True)

    if ban:
        if ban.user_message:
            raise ValidationError(ban.user_message)
        else:
            raise ValidationError(
                pgettext_lazy("username validator", "This username is not allowed.")
            )


def validate_username_content(value):
    if not USERNAME_RE.match(value):
        raise ValidationError(
            pgettext_lazy(
                "username validator",
                "Username can only contain Latin alphabet letters, digits, and an underscore sign.",
            )
        )

    if not USERNAME_LATIN_ALPHA_RE.search(value):
        raise ValidationError(
            pgettext_lazy(
                "username validator",
                "Username must contain Latin alphabet letters or digits.",
            )
        )


def validate_username_length(settings, value):
    if len(value) < settings.username_length_min:
        message = npgettext(
            "username length validator",
            "Username must be at least %(limit_value)s character long.",
            "Username must be at least %(limit_value)s characters long.",
            settings.username_length_min,
        )
        raise ValidationError(message % {"limit_value": settings.username_length_min})

    if len(value) > settings.username_length_max:
        message = npgettext(
            "username length validator",
            "Username cannot be longer than %(limit_value)s characters.",
            "Username cannot be longer than %(limit_value)s characters.",
            settings.username_length_max,
        )
        raise ValidationError(message % {"limit_value": settings.username_length_max})


# New account validators
SFS_API_URL = (
    "http://api.stopforumspam.org/api?email=%(email)s&ip=%(ip)s&f=json&confidence"
)


def validate_with_sfs(request, cleaned_data, add_error):
    if request.settings.enable_stop_forum_spam and cleaned_data.get("email"):
        try:
            _real_validate_with_sfs(
                request.user_ip,
                cleaned_data["email"],
                request.settings.stop_forum_spam_confidence,
            )
        except RequestException as error:
            logger.exception(error, exc_info=error)


def _real_validate_with_sfs(ip, email, confidence):
    r = requests.get(SFS_API_URL % {"email": email, "ip": ip}, timeout=5)
    r.raise_for_status()

    api_response = json.loads(force_str(r.content))
    ip_score = api_response.get("ip", {}).get("confidence", 0)
    email_score = api_response.get("email", {}).get("confidence", 0)

    api_score = max((ip_score, email_score))

    if api_score > confidence:
        raise ValidationError(
            pgettext_lazy(
                "stop forum spam validator",
                "Data entered was found in spammers database.",
            )
        )


def validate_gmail_email(request, cleaned_data, add_error):
    email = cleaned_data.get("email", "")
    if "@" not in email:
        return

    username, domain = email.lower().split("@")
    if domain == "gmail.com" and username.count(".") > 5:
        add_error(
            "email",
            ValidationError(
                pgettext_lazy("gmail email validator", "This e-mail is not allowed.")
            ),
        )


# Registration validation
validators_list = settings.MISAGO_NEW_REGISTRATIONS_VALIDATORS
REGISTRATION_VALIDATORS = list(map(import_string, validators_list))


def raise_validation_error(*_):
    raise ValidationError("")  # Raised when message content can be discarded


def validate_new_registration(request, cleaned_data, add_error=None, validators=None):
    validators = validators or REGISTRATION_VALIDATORS

    add_error = add_error or raise_validation_error
    for validator in validators:
        validator(request, cleaned_data, add_error)
    for validator in hooks.new_registrations_validators:
        validator(request, cleaned_data, add_error)
