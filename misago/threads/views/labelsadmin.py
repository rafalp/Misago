from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from misago.admin.views import generic
from misago.core import cachebuster

from misago.threads.models import Label
from misago.threads.forms.admin import LabelForm


class LabelsAdmin(generic.AdminBaseMixin):
    root_link = 'misago:admin:forums:labels:index'
    Model = Label
    Form = LabelForm
    templates_dir = 'misago/admin/labels'
    message_404 = _("Requested thread label does not exist.")

    def handle_form(self, form, request, target):
        target.save()
        target.forums.clear()
        if form.cleaned_data.get('forums'):
            target.forums.add(*[f for f in form.cleaned_data.get('forums')])
        Label.objects.clear_cache()

        if self.message_submit:
            messages.success(request, self.message_submit % target.name)


class LabelsList(LabelsAdmin, generic.ListView):
    ordering = (('name', None),)


class NewLabel(LabelsAdmin, generic.ModelFormView):
    message_submit = _('New label "%s" has been saved.')


class EditLabel(LabelsAdmin, generic.ModelFormView):
    message_submit = _('Label "%s" has been edited.')


class DeleteLabel(LabelsAdmin, generic.ButtonView):
    def button_action(self, request, target):
        target.delete()
        message = _('Label "%s" has been deleted.')
        messages.success(request, message % unicode(target.name))
