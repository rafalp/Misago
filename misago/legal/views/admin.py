from django.contrib import messages
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from misago.admin.views import generic

from misago.legal.forms import AgreementForm, SearchAgreementsForm
from misago.legal.models import Agreement
from misago.legal.utils import set_agreement_as_active


class AgreementAdmin(generic.AdminBaseMixin):
    root_link = 'misago:admin:users:agreements:index'
    model = Agreement
    form = AgreementForm
    templates_dir = 'misago/admin/agreements'
    message_404 = _("Requested agreement does not exist.")

    def handle_form(self, form, request, target):
        form.save()
        
        if self.message_submit:
            messages.success(request, self.message_submit % {'title': target.get_final_title()})


class AgreementsList(AgreementAdmin, generic.ListView):
    items_per_page = 30
    ordering = [
        ('-id', _("From newest")),
        ('id', _("From oldest")),
    ]
    search_form = SearchAgreementsForm
    selection_label = _('With agreements: 0')
    empty_selection_label = _('Select agreements')
    mass_actions = ({
        'action': 'delete',
        'icon': 'fa fa-times',
        'name': _('Delete agreements'),
        'confirmation': _('Are you sure you want to delete those agreements?')
    }, )

    def get_queryset(self):
        qs = super(AgreementsList, self).get_queryset()
        return qs.select_related()

    def action_delete(self, request, items):
        items.delete()
        Agreement.objects.invalidate_cache()
        messages.success(request, _("Selected agreements have been deleted."))


class NewAgreement(AgreementAdmin, generic.ModelFormView):
    message_submit = _('New agreement "%(title)s" has been saved.')
    
    def handle_form(self, form, request, target):
        super(NewAgreement, self).handle_form(form, request, target)

        form.instance.set_created_by(request.user)
        form.instance.save()


class EditAgreement(AgreementAdmin, generic.ModelFormView):
    message_submit = _('Agreement "%(title)s" has been edited.')

    def handle_form(self, form, request, target):
        super(EditAgreement, self).handle_form(form, request, target)

        form.instance.last_modified_on = timezone.now()
        form.instance.set_last_modified_by(request.user)
        form.instance.save()


class DeleteAgreement(AgreementAdmin, generic.ButtonView):
    def button_action(self, request, target):
        target.delete()
        Agreement.objects.invalidate_cache()
        message = _('Agreement "%(title)s" has been deleted.')
        messages.success(request, message % {'title': target.get_final_title()})


class SetAgreementAsActive(AgreementAdmin, generic.ButtonView):
    def button_action(self, request, target):
        set_agreement_as_active(target, commit=True)

        message = _('Agreement "%(title)s" has been set as active for type "%(type)s".')
        targets_names = {'title': target.get_final_title(), 'type': target.get_type_display()}
        messages.success(request, message % targets_names)