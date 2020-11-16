import re

from django.forms import (
    CharField,
    DateTimeField,
    RadioSelect,
    TypedChoiceField,
    ValidationError,
)
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from ..core.utils import parse_iso8601_string


class IsoDateTimeField(DateTimeField):
    input_formats = ["iso8601"]

    def prepare_value(self, value):
        try:
            return value.isoformat()
        except AttributeError:
            return value

    def to_python(self, value):
        """
        Validates that the input can be converted to a datetime. Returns a
        Python datetime.datetime object.
        """
        if value in self.empty_values:
            return None

        try:
            return parse_iso8601_string(value)
        except ValueError:
            raise ValidationError(self.error_messages["invalid"], code="invalid")


def ColorField(**kwargs):
    return CharField(
        validators=[
            RegexValidator(
                r"^#[0-9a-f]{6}$",
                flags=re.IGNORECASE,
                message=_(
                    "Value must be a 7-character string specifying an RGB color "
                    "in a hexadecimal format."
                ),
            )
        ],
        **kwargs
    )


class YesNoSwitchBase(TypedChoiceField):
    def prepare_value(self, value):
        """normalize bools to binary 1/0 so field works on them too"""
        if value in (True, "True", "true", 1, "1"):
            return 1
        return 0

    def clean(self, value):
        return self.prepare_value(value)


def YesNoSwitch(**kwargs):
    yes_label = kwargs.pop("yes_label", _("Yes"))
    no_label = kwargs.pop("no_label", _("No"))

    return YesNoSwitchBase(
        coerce=int,
        choices=[(1, yes_label), (0, no_label)],
        widget=RadioSelect(attrs={"class": "yesno-switch"}),
        **kwargs
    )
