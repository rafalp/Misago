from django.forms import *  # noqa
from django.forms import Form as BaseForm, ModelForm as BaseModelForm


class AutoStripWhitespacesMixin(object):
    autostrip_exclude = []

    def full_clean(self):
        self.data = self.data.copy()
        for name, field in self.fields.iteritems():
            if (field.__class__ == CharField and
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
