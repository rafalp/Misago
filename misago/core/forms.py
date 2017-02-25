from django.forms import DateTimeField, RadioSelect, TypedChoiceField, ValidationError
from django.utils.translation import ugettext_lazy as _

from .utils import parse_iso8601_string


class IsoDateTimeField(DateTimeField):
    input_formats = ['iso8601']

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
            raise ValidationError(self.error_messages['invalid'], code='invalid')


class YesNoSwitchBase(TypedChoiceField):
    def prepare_value(self, value):
        """normalize bools to binary 1/0 so field works on them too"""
        if value in (True, 'True', 'true', 1, '1'):
            return 1
        else:
            return 0

    def clean(self, value):
        return self.prepare_value(value)


def YesNoSwitch(**kwargs):
    yes_label = kwargs.pop('yes_label', _("Yes"))
    no_label = kwargs.pop('no_label', _("No"))

    return YesNoSwitchBase(
        coerce=int,
        choices=[
            (1, yes_label),
            (0, no_label),
        ],
        widget=RadioSelect(attrs={'class': 'yesno-switch'}),
        **kwargs
    )
