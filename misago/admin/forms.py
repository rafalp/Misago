import re

from django.core.validators import RegexValidator
from django.db.models import CharField
from django.forms import (
    CharField,
    DateTimeField,
    RadioSelect,
    TypedChoiceField,
    ValidationError,
)
from django.utils.translation import pgettext_lazy

from ..core.utils import parse_iso8601_string
from ..permissions.enums import PermissionValue


def ColorField(**kwargs):
    return CharField(
        validators=[
            RegexValidator(
                r"^#[0-9a-f]{6}$",
                flags=re.IGNORECASE,
                message=pgettext_lazy(
                    "admin color field",
                    'Value must be a 7-character string specifying an RGB color in a hexadecimal format (eg.: "#F5A9B8").',
                ),
            )
        ],
        **kwargs,
    )


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


class YesNoFieldBase(TypedChoiceField):
    def prepare_value(self, value):
        """normalize bools to binary 1/0 so field works on them too"""
        if value in (True, "True", "true", 1, "1"):
            return 1
        return 0

    def clean(self, value):
        return self.prepare_value(value)


def YesNoField(**kwargs):
    yes_label = kwargs.pop("yes_label", pgettext_lazy("admin yesno switch", "Yes"))
    no_label = kwargs.pop("no_label", pgettext_lazy("admin yesno switch", "No"))

    return YesNoFieldBase(
        coerce=int,
        choices=[(1, yes_label), (0, no_label)],
        widget=RadioSelect,
        **kwargs
    )


class YesNoNeverField(TypedChoiceField):
    def __init__(self, *args, **kwargs):
        return super().__init__(
            *args,
            coerce=int,
            choices=PermissionValue.get_choices(),
            widget=RadioSelect,
            **kwargs
        )
