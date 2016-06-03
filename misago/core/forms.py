from datetime import datetime, timedelta

from mptt.forms import *  # noqa

from django.forms import *  # noqa
from django.forms import Form as BaseForm, ModelForm as BaseModelForm
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _


TEXT_BASED_FIELDS = (
    CharField, EmailField, FilePathField, URLField
)


"""
Fields
"""
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
        choices=((1, yes_label), (0, no_label)),
        widget=RadioSelect(attrs={'class': 'yesno-switch'}),
        **kwargs)


class IsoDateTimeField(DateTimeField):
    input_formats = ['iso8601']
    iso8601_formats = (
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S+00:00",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S.%f+00:00")

    def prepare_value(self, value):
        try:
            return value.isoformat()
        except AttributeError:
            return value

    def strptime(self, value):
        for format in self.iso8601_formats:
            try:
                return datetime.strptime(value, format)
            except ValueError:
                pass
        else:
            raise ValueError()

    def to_python(self, value):
        """
        Validates that the input can be converted to a datetime. Returns a
        Python datetime.datetime object.
        """
        if value in self.empty_values:
            return None

        try:
            unicode_value = force_text(value, strings_only=True)
            date = unicode_value[:-6]
            offset = unicode_value[-6:]

            local_date = self.strptime(value)

            if offset and offset[0] in ('-', '+'):
                tz_offset = timedelta(hours=int(offset[1:3]),
                                      minutes=int(offset[4:6]))
                tz_offset = tz_offset.seconds // 60
                if offset[0] == '-':
                    tz_offset *= -1
            else:
                tz_offset = 0

            tz_correction = timezone.get_fixed_timezone(tz_offset)
            return timezone.make_aware(local_date, tz_correction)
        except (IndexError, TypeError, ValueError) as e:
            raise ValidationError(
                self.error_messages['invalid'], code='invalid')


"""
Forms
"""
class Form(BaseForm):
    pass


class ModelForm(BaseModelForm):
    pass
