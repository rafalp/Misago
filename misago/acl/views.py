from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from misago.admin.views import generic
from misago.acl import get_change_permissions_forms
from misago.acl.forms import RoleForm
from misago.acl.models import Role


class RoleAdmin(generic.AdminBaseMixin):
    root_link = 'misago:admin:permissions:users:index'
    Model = Role
    templates_dir = 'misago/admin/roles'
    message_404 = _("Requested role does not exist.")


class RolesList(RoleAdmin, generic.ListView):
    ordering = (('name', None),)


class RoleFormMixin(object):
    def real_dispatch(self, request, target):
        role_permissions = target.permissions
        form = RoleForm(instance=target)

        perms_forms = get_change_permissions_forms(target)

        if request.method == 'POST':
            perms_forms = get_change_permissions_forms(target, request.POST)
            valid_forms = 0
            for permissions_form in perms_forms:
                if permissions_form.is_valid():
                    valid_forms += 1

            form = RoleForm(request.POST, instance=target)
            if form.is_valid() and len(perms_forms) == valid_forms:
                new_permissions = {}
                for permissions_form in perms_forms:
                    cleaned_data = permissions_form.cleaned_data
                    new_permissions[permissions_form.prefix] = cleaned_data

                form.instance.permissions = new_permissions
                form.instance.save()

                messages.success(request, self.message_submit % target.name)

                if 'stay' in request.POST:
                    return redirect(request.path)
                else:
                    return redirect(self.root_link)
        else:
            perms_forms = get_change_permissions_forms(target)

        return self.render(
            request,
            {
                'form': form,
                'target': target,
                'perms_forms': perms_forms,
            })


class NewRole(RoleFormMixin, RoleAdmin, generic.ModelFormView):
    message_submit = _('New role "%s" has been saved.')


class EditRole(RoleFormMixin, RoleAdmin, generic.ModelFormView):
    message_submit = _('Role "%s" has been changed.')


class DeleteRole(RoleAdmin, generic.ButtonView):
    def button_action(self, request, target):
        target.delete()
        message = _('Role "%s" has been deleted.') % unicode(target.name)
        messages.success(request, message)
