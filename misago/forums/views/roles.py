from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from misago.admin.views import generic
from misago.acl import get_change_permissions_forms
from misago.acl.views import RoleAdmin, RolesList
from misago.forums.forms import ForumRoleForm
from misago.forums.models import ForumRole


class ForumRoleAdmin(generic.AdminBaseMixin):
    root_link = 'misago:admin:permissions:forums:index'
    Model = ForumRole
    templates_dir = 'misago/admin/forumroles'
    message_404 = _("Requested role does not exist.")


class ForumRolesList(ForumRoleAdmin, generic.ListView):
    ordering = (('name', None),)


class RoleFormMixin(object):
    def real_dispatch(self, request, target):
        role_permissions = target.permissions
        form = ForumRoleForm(instance=target)

        perms_forms = get_change_permissions_forms(target)

        if request.method == 'POST':
            perms_forms = get_change_permissions_forms(target, request.POST)
            valid_forms = 0
            for permissions_form in perms_forms:
                if permissions_form.is_valid():
                    valid_forms += 1

            form = ForumRoleForm(request.POST, instance=target)
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


class NewForumRole(RoleFormMixin, ForumRoleAdmin, generic.ModelFormView):
    message_submit = _('New role "%s" has been saved.')


class EditForumRole(RoleFormMixin, ForumRoleAdmin, generic.ModelFormView):
    message_submit = _('Role "%s" has been changed.')


class DeleteForumRole(ForumRoleAdmin, generic.ButtonView):
    def button_action(self, request, target):
        target.delete()
        message = _('Role "%s" has been deleted.') % unicode(target.name)
        messages.success(request, message)


"""
Create forums perms view for perms role and register it in other admin
"""
class RoleForumsACL(RoleAdmin, generic.ModelFormView):
    templates_dir = 'misago/admin/forumroles'
    template = 'forumsroles.html'


RolesList.add_item_action(
    name=_("Forums permissions"),
    icon='fa fa-comments-o',
    link='misago:admin:permissions:users:forums')
