from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from misago.admin.views import generic
from misago.core import cachebuster

from misago.threads.models import Prefix
from misago.threads.forms.admin import PrefixForm


class PrefixesAdmin(generic.AdminBaseMixin):
    root_link = 'misago:admin:forums:prefixes:index'
    Model = Prefix
    Form = PrefixForm
    templates_dir = 'misago/admin/prefixes'
    message_404 = _("Requested thread prefix does not exist.")

    def handle_form(self, form, request, target):
        target.save()
        target.forums.clear()
        if form.cleaned_data.get('forums'):
            target.forums.add(*[f for f in form.cleaned_data.get('forums')])
        Prefix.objects.clear_cache()

        if self.message_submit:
            messages.success(request, self.message_submit % target.name)


class PrefixesList(PrefixesAdmin, generic.ListView):
    ordering = (('name', None),)


class NewPrefix(PrefixesAdmin, generic.ModelFormView):
    message_submit = _('New prefix "%s" has been saved.')


class EditPrefix(PrefixesAdmin, generic.ModelFormView):
    message_submit = _('Prefix "%s" has been edited.')


class DeletePrefix(PrefixesAdmin, generic.ButtonView):
    def button_action(self, request, target):
        target.delete()
        message = _('Prefix "%s" has been deleted.')
        messages.success(request, message % unicode(target.name))
