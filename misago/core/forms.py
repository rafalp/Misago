from floppyforms import *
from floppyforms import Form as BaseForm, ModelForm as BaseModelForm


class AutoStripInputMixin(object):
    autostrip_exclude = None

    def full_clean(self):
        self.data = self.data.copy()
        for name, field in self.fields.iteritems():
            if (field.__class__ == CharField and
                    not name in self.autostrip_exclude):
                try:
                    self.data[name] = self.data[name].strip()
                except KeyError:
                    pass
        return super(AutoStripInputMixin, self).full_clean()


class Form(AutoStripInputMixin, BaseForm):
    pass


class ModelForm(AutoStripInputMixin, BaseModelForm):
    pass
