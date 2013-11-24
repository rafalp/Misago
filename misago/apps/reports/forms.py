from django import forms
from django.utils.translation import ugettext_lazy as _
from misago.apps.threadtype.posting.forms import (EditThreadForm as EditThreadBaseForm,
                                                  NewReplyForm as NewReplyBaseForm,
                                                  EditReplyForm as EditReplyBaseForm)
from misago.forms import Form

class ReportFormMixin(object):
    def type_fields(self):
        self.thread.original_weight = self.thread.weight

        thread_weight = []
        if self.thread.weight == 2:
            thread_weight.append((2, _("Unresolved")))
        thread_weight.append((1, _("Resolved")))
        thread_weight.append((0, _("Bogus")))

        self.fields['thread_weight'].choices = thread_weight


class EditThreadForm(ReportFormMixin, EditThreadBaseForm):
    pass


class NewReplyForm(ReportFormMixin, NewReplyBaseForm):
    pass


class EditReplyForm(ReportFormMixin, EditReplyBaseForm):
    pass