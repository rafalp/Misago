from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from misago.admin.views import generic
from misago.acl.models import Role
from misago.acl.forms import RoleForm


class RoleAdmin(generic.AdminBaseMixin):
    root_link = 'misago:admin:permissions:users:index'
    Model = Role
    Form = RoleForm
    templates_dir = 'misago/admin/roles'
    message_404 = _("Requested role does not exist.")


class RolesList(RoleAdmin, generic.ListView):
    ordering = (('name', None),)


class NewRole(RoleAdmin, generic.ModelFormView):
    message_submit = _('New role "%s" has been saved.')


class EditRole(RoleAdmin, generic.ModelFormView):
    message_submit = _('Role "%s" has been changed.')


class DeleteRole(RoleAdmin, generic.ButtonView):
    def button_action(self, request, target):
        target.delete()
        message = _('Role "%s" has been deleted.') % unicode(target.name)
        messages.success(request, message)
