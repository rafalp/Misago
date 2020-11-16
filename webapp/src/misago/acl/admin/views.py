from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...admin.views import generic
from ..models import Role
from .forms import RoleForm, get_permissions_forms


class RoleAdmin(generic.AdminBaseMixin):
    root_link = "misago:admin:permissions:index"
    model = Role
    templates_dir = "misago/admin/roles"
    message_404 = _("Requested role does not exist.")


class RolesList(RoleAdmin, generic.ListView):
    ordering = (("name", None),)


class RoleFormMixin:
    def real_dispatch(self, request, target):
        form = RoleForm(instance=target)

        perms_forms = get_permissions_forms(target)

        if request.method == "POST":
            perms_forms = get_permissions_forms(target, request.POST)
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

                messages.success(request, self.message_submit % {"name": target.name})

                if "stay" in request.POST:
                    return redirect(request.path)
                return redirect(self.root_link)
            if form.is_valid() and len(perms_forms) != valid_forms:
                form.add_error(None, _("Form contains errors."))

        template_name = self.get_template_name(request, target)
        return self.render(
            request,
            {"form": form, "target": target, "perms_forms": perms_forms},
            template_name,
        )


class NewRole(RoleFormMixin, RoleAdmin, generic.ModelFormView):
    message_submit = _('New role "%(name)s" has been saved.')


class EditRole(RoleFormMixin, RoleAdmin, generic.ModelFormView):
    message_submit = _('Role "%(name)s" has been changed.')


class DeleteRole(RoleAdmin, generic.ButtonView):
    def check_permissions(self, request, target):
        if target.special_role:
            message = _('Role "%(name)s" is special role and can\'t be deleted.')
            return message % {"name": target.name}

    def button_action(self, request, target):
        target.delete()
        message = _('Role "%(name)s" has been deleted.')
        messages.success(request, message % {"name": target.name})


class RoleUsers(RoleAdmin, generic.TargetedView):
    def real_dispatch(self, request, target):
        redirect_url = reverse("misago:admin:users:index")
        return redirect("%s?role=%s" % (redirect_url, target.pk))
