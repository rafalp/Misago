from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from misago.admin.views import generic
from misago.users.forms.admin import BanForm, SearchBansForm
from misago.users.models import Ban


class BanAdmin(generic.AdminBaseMixin):
    root_link = 'misago:admin:users:bans:index'
    model = Ban
    form = BanForm
    templates_dir = 'misago/admin/bans'
    message_404 = _("Requested ban does not exist.")

    def handle_form(self, form, request, target):
        super(BanAdmin, self).handle_form(form, request, target)
        Ban.objects.invalidate_cache()


class BansList(BanAdmin, generic.ListView):
    items_per_page = 30
    ordering = [
        ('-id', _("From newest")),
        ('id', _("From oldest")),
        ('banned_value', _("A to z")),
        ('-banned_value', _("Z to a")),
    ]
    search_form = SearchBansForm
    selection_label = _('With bans: 0')
    empty_selection_label = _('Select bans')
    mass_actions = ({
        'action': 'delete',
        'icon': 'fa fa-times',
        'name': _('Remove bans'),
        'confirmation': _('Are you sure you want to remove those bans?')
    }, )

    def action_delete(self, request, items):
        items.delete()
        Ban.objects.invalidate_cache()
        messages.success(request, _("Selected bans have been removed."))


class NewBan(BanAdmin, generic.ModelFormView):
    message_submit = _('New ban "%(name)s" has been saved.')


class EditBan(BanAdmin, generic.ModelFormView):
    message_submit = _('Ban "%(name)s" has been edited.')


class DeleteBan(BanAdmin, generic.ButtonView):
    def button_action(self, request, target):
        target.delete()
        Ban.objects.invalidate_cache()
        message = _('Ban "%(name)s" has been removed.')
        messages.success(request, message % {'name': target.name})
