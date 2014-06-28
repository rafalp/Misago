from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from misago.admin.views import generic
from misago.core import cachebuster
from misago.users.models import Ban
from misago.users.forms.admin import SearchBansForm, BanForm


class BanAdmin(generic.AdminBaseMixin):
    root_link = 'misago:admin:users:bans:index'
    Model = Ban
    Form = BanForm
    templates_dir = 'misago/admin/bans'
    message_404 = _("Requested ban does not exist.")

    def handle_form(self, form, request, target):
        super(BanAdmin, self).handle_form(form, request, target)
        cachebuster.invalidate('misago_bans')


class BansList(BanAdmin, generic.ListView):
    items_per_page = 30
    ordering = (
        ('-id', _("From newest")),
        ('id', _("From oldest")),
        ('banned_value', _("A to z")),
        ('-banned_value', _("Z to a")),
    )
    SearchForm = SearchBansForm
    selection_label = _('With bans: 0')
    empty_selection_label = _('Select bans')
    mass_actions = (
        (
            'delete',
            _('Remove bans'),
            _('Are you sure you want to remove those bans?')
        ),
    )

    def action_delete(self, request, items):
        items.delete()
        cachebuster.invalidate('misago_bans')
        messages.success(request, _("Selected bans have been removed."))


class NewBan(BanAdmin, generic.ModelFormView):
    message_submit = _('New ban "%s" has been saved.')


class EditBan(BanAdmin, generic.ModelFormView):
    message_submit = _('Ban "%s" has been edited.')


class DeleteBan(BanAdmin, generic.ButtonView):
    def button_action(self, request, target):
        target.delete()
        cachebuster.invalidate('misago_bans')
        message = _('Ban "%s" has been removed.') % unicode(target.name)
        messages.success(request, message)
