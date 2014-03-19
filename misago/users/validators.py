import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model


username_regex = re.compile(r'^[0-9A-Z]+$', re.IGNORECASE)


def validate_username_available(value):
    User = get_user_model()


def validate_username_content(value):
    if not username_regex.match(value):
        raise ValidationError(
            _("Username can only contain latin alphabet letters and digits."))


def validate_username_length(value):
    pass


def validate_username(value):
    validate_username_available(value)
    validate_username_content(value)
    validate_username_length(value)
