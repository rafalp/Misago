from crispy_forms.helper import FormHelper
from django.utils.translation import ugettext_lazy as _
from django.forms import *  # noqa
from django.forms import Form as BaseForm, ModelForm as BaseModelForm


TEXT_BASED_FIELDS = (
    CharField, EmailField, FilePathField, URLField
)


class YesNoSwitchBase(TypedChoiceField):
    def prepare_value(self, value):
        """normalize bools to binary 1/0 so field works on them too"""
        return 1 if value else 0

    def clean(self, value):
        value = 1 if value else 0
        return super(YesNoSwitchBase, self).clean(value)


def YesNoSwitch(**kwargs):
    if 'initial' not in kwargs:
        kwargs['initial'] = 0

    kwargs['initial'] = 1 if kwargs['initial'] else 0

    return YesNoSwitchBase(
        coerce=int,
        choices=((1, _("Yes")), (0, _("No"))),
        widget=RadioSelect(attrs={'class': 'yesno-switch'}),
        **kwargs)


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
