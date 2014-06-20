from django.utils.translation import ugettext_lazy as _
from django.forms import *  # noqa
from django.forms import Form as BaseForm, ModelForm as BaseModelForm
from crispy_forms.helper import FormHelper


TEXT_BASED_FIELDS = (
    CharField, EmailField, FilePathField, URLField
)


def YesNoSwitch(**kwargs):
    if 'initial' not in kwargs:
        kwargs['initial'] = 0

    if kwargs['initial'] == True:
        kwargs['initial'] = 1
    if kwargs['initial'] == False:
        kwargs['initial'] = 0

    return TypedChoiceField(
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
