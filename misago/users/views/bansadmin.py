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

    def update_roles(self, target, roles):
        target.roles.clear()
        if roles:
            target.roles.add(*roles)

    def handle_form(self, form, request, target):
        super(BanAdmin, self).handle_form(form, request, target)
        cachebuster.invalidate('misago_bans')


class BansList(BanAdmin, generic.ListView):
    ordering = (('-id', None),)


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
