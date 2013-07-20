import copy
from django.core.urlresolvers import reverse as django_reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago import messages
from misago.acl.builder import build_form
from misago.admin import site
from misago.apps.admin.widgets import *
from misago.forms import Form, YesNoSwitch
from misago.models import Forum, ForumRole, Role
from misago.monitor import monitor, UpdatingMonitor
from misago.utils.strings import slugify
from misago.apps.admin.roles.forms import RoleForm

def reverse(route, target=None):
    if target:
        return django_reverse(route, kwargs={'target': target.pk, 'slug': slugify(target.name)})
    return django_reverse(route)


"""
Views
"""
class List(ListWidget):
    admin = site.get_action('roles')
    id = 'list'
    columns=(
             ('role', _("Role")),
             )
    nothing_checked_message = _('You have to check at least one role.')
    actions=(
             ('delete', _("Delete selected roles"), _("Are you sure you want to delete selected roles?")),
             )

    def sort_items(self, page_items, sorting_method):
        return page_items.order_by('name')

    def get_item_actions(self, item):
        return (
                self.action('list', _("Forums Permissions"), reverse('admin_roles_masks', item)),
                self.action('adjust', _("Role Permissions"), reverse('admin_roles_acl', item)),
                self.action('pencil', _("Edit Role"), reverse('admin_roles_edit', item)),
                self.action('remove', _("Delete Role"), reverse('admin_roles_delete', item), post=True, prompt=_("Are you sure you want to delete this role?")),
                )

    def action_delete(self, items, checked):
        for item in items:
            if item.pk in checked:
                if item.special:
                    return Message(_('You cannot delete system roles.'), 'error'), reverse('admin_roles')
                if item.protected and not self.request.user.is_god():
                    return Message(_('You cannot delete protected roles.'), 'error'), reverse('admin_roles')
                if item.user_set.count() > 0:
                    return Message(_('You cannot delete roles that are assigned to users.'), 'error'), reverse('admin_roles')

        Role.objects.filter(id__in=checked).delete()
        return Message(_('Selected roles have been deleted successfully.'), 'success'), reverse('admin_roles')


class New(FormWidget):
    admin = site.get_action('roles')
    id = 'new'
    fallback = 'admin_roles'
    form = RoleForm
    submit_button = _("Save Role")

    def get_new_link(self, model):
        return reverse('admin_roles_new')

    def get_edit_link(self, model):
        return reverse('admin_roles_edit', model)

    def submit_form(self, form, target):
        new_role = Role(name=form.cleaned_data['name'])
        new_role.save(force_insert=True)
        return new_role, Message(_('New Role has been created.'), 'success')


class Edit(FormWidget):
    admin = site.get_action('roles')
    id = 'edit'
    name = _("Edit Role")
    fallback = 'admin_roles'
    form = RoleForm
    target_name = 'name'
    translate_target_name = True
    notfound_message = _('Requested Role could not be found.')
    submit_fallback = True

    def get_link(self, model):
        return reverse('admin_roles_edit', model)

    def get_edit_link(self, model):
        return self.get_link(model)

    def get_initial_data(self, model):
        if self.request.user.is_god():
            return {'name': model.name, 'protected': model.protected}
        return {'name': model.name}

    def get_and_validate_target(self, target):
        result = super(Edit, self).get_and_validate_target(target)
        if result and result.protected and not self.request.user.is_god():
            messages.error(self.request, _('Role "%(name)s" is protected, you cannot edit it.') % {'name': _(result.name)}, self.admin.id)
            return None
        return result

    def submit_form(self, form, target):
        target.name = form.cleaned_data['name']
        if self.request.user.is_god():
            target.protected = form.cleaned_data['protected']
        target.save(force_update=True)
        with UpdatingMonitor() as cm:
            monitor.increase('acl_version')
        return target, Message(_('Changes in role "%(name)s" have been saved.') % {'name': self.original_name}, 'success')


class Forums(ListWidget):
    admin = site.get_action('roles')
    id = 'forums'
    hide_actions = True
    name = _('Role Forums Permissions')
    table_form_button = _('Change Permissions')
    empty_message = _('No forums are currently defined.')
    template = 'forums'

    def get_link(self):
        return reverse('admin_roles_masks', self.role)

    def get_items(self):
        return Forum.objects.get(special='root').get_descendants()

    def sort_items(self, page_items, sorting_method):
        return page_items.order_by('lft').all()

    def add_template_variables(self, variables):
        variables['target'] = _(self.role.name)
        return variables

    def get_table_form(self, page_items):
        perms = {}
        try:
            forums = self.role.permissions['forums']
            for fid in forums:
               perms[str(fid)] = str(forums[fid])
        except KeyError:
            pass

        perms_form = {}
        roles_select = [("0", _("No Access"))]
        for role in self.roles:
            roles_select.append((str(role.pk), _(role.name)))

        for item in page_items:
            perms_form['forum_' + str(item.pk)] = forms.ChoiceField(choices=roles_select,initial=(perms[str(item.pk)] if str(item.pk) in perms else "0"))

        # Turn dict into object
        return type('ChangeForumRolesForm', (Form,), perms_form)

    def table_action(self, page_items, cleaned_data):
        perms = {}
        for item in page_items:
            if cleaned_data['forum_' + str(item.pk)] != "0":
                perms[item.pk] = long(cleaned_data['forum_' + str(item.pk)])
        role_perms = self.role.permissions
        role_perms['forums'] = perms
        self.role.permissions = role_perms
        self.role.save(force_update=True)
        return Message(_('Forum permissions have been saved.'), 'success'), self.get_link()

    def __call__(self, request, slug, target):
        self.request = request
        try:
            self.role = Role.objects.get(id=target)
            if self.role and self.role.protected and not request.user.is_god():
                messages.error(request, _('Role "%(name)s" is protected, you cannot edit it.') % {'name': _(self.role.name)}, self.admin.id)
                return redirect(reverse('admin_roles'))
        except Role.DoesNotExist:
            messages.error(request, _('Requested Role could not be found.'), self.admin.id)
            return redirect(reverse('admin_roles'))
        self.roles = ForumRole.objects.order_by('name').all()
        if not self.roles:
            messages.error(request, _('No forum roles are currently set.'), self.admin.id)
            return redirect(reverse('admin_roles'))
        return super(Forums, self).__call__(request)


class ACL(FormWidget):
    admin = site.get_action('roles')
    id = 'acl'
    name = _("Change Role Permissions")
    fallback = 'admin_roles'
    target_name = 'name'
    translate_target_name = True
    notfound_message = _('Requested Role could not be found.')
    submit_fallback = True
    template = 'acl_form'

    def get_form(self, target):
        self.form = build_form(self.request, target)
        return self.form

    def get_link(self, model):
        return reverse('admin_roles_acl', model)

    def get_edit_link(self, model):
        return self.get_link(model)

    def get_initial_data(self, model):
        raw_acl = model.permissions
        initial = {}
        for field in self.form.base_fields:
            if field in raw_acl:
                initial[field] = raw_acl[field]
        return initial

    def get_and_validate_target(self, target):
        result = super(ACL, self).get_and_validate_target(target)
        if result and result.protected and not self.request.user.is_god():
            messages.error(self.request, _('Role "%(name)s" is protected, you cannot edit it.') % {'name': _(result.name)}, self.admin.id)
            return None
        return result

    def submit_form(self, form, target):
        raw_acl = target.permissions
        for perm in form.cleaned_data:
            raw_acl[perm] = form.cleaned_data[perm]
        target.permissions = raw_acl
        target.save(force_update=True)
        with UpdatingMonitor() as cm:
            monitor.increase('acl_version')

        return target, Message(_('Role "%(name)s" permissions have been changed.') % {'name': self.original_name}, 'success')


class Delete(ButtonWidget):
    admin = site.get_action('roles')
    id = 'delete'
    fallback = 'admin_roles'
    notfound_message = _('Requested Role could not be found.')

    def action(self, target):
        if target.special:
            return Message(_('You cannot delete system roles.'), 'error'), reverse('admin_roles')
        if target.protected and not self.request.user.is_god():
            return Message(_('This role is protected.'), 'error'), reverse('admin_roles')
        if target.user_set.count() > 0:
            return Message(_('This role is assigned to one or more users.'), 'error'), reverse('admin_roles')

        target.delete()
        return Message(_('Role "%(name)s" has been deleted.') % {'name': _(target.name)}, 'success'), False