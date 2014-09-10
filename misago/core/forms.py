from mptt.forms import *  # noqa

from django.forms import *  # noqa
from django.forms import Form as BaseForm, ModelForm as BaseModelForm
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
        return 1 if value in [True, 'True', 1, '1'] else 0

    def clean(self, value):
        return self.prepare_value(value)


def YesNoSwitch(**kwargs):
    yes_label = kwargs.pop('yes_label', _("Yes"))
    no_label = kwargs.pop('yes_label', _("No"))

    return YesNoSwitchBase(
        coerce=int,
        choices=((1, yes_label), (0, no_label)),
        widget=RadioSelect(attrs={'class': 'yesno-switch'}),
        **kwargs)


"""
Forms
"""
class AutoStripWhitespacesMixin(object):
    autostrip_exclude = []

    def full_clean(self):
        self.data = self.data.copy()
        for name, field in self.fields.iteritems():
            if (field.__class__ in TEXT_BASED_FIELDS and
                    not name in self.autostrip_exclude):
                try:
                    self.data[name] = self.data[name].strip()
                except KeyError:
                    pass
        return super(AutoStripWhitespacesMixin, self).full_clean()


class Form(AutoStripWhitespacesMixin, BaseForm):
    pass


class ModelForm(AutoStripWhitespacesMixin, BaseModelForm):
    pass
