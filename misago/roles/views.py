import copy
from django.core.urlresolvers import reverse as django_reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago.acl.builder import build_form 
from misago.admin import site
from misago.admin.widgets import *
from misago.utils import slugify
from misago.forms import Form, YesNoSwitch
from misago.forums.models import Forum
from misago.forumroles.models import ForumRole
from misago.roles.forms import RoleForm
from misago.roles.models import Role

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
            if unicode(item.pk) in checked:
                if item.token:
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
        
    def get_new_url(self, model):
        return reverse('admin_roles_new')
    
    def get_edit_url(self, model):
        return reverse('admin_roles_edit', model)
    
    def submit_form(self, form, target):
        new_role = Role(
                      name = form.cleaned_data['name'],
                     )
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
    
    def get_url(self, model):
        return reverse('admin_roles_edit', model)
    
    def get_edit_url(self, model):
        return self.get_url(model)
    
    def get_initial_data(self, model):
        if self.request.user.is_god():
            return {'name': model.name, 'protected': model.protected}
        return {'name': model.name}
    
    def get_and_validate_target(self, target):
        result = super(Edit, self).get_and_validate_target(target)
        if result and result.protected and not self.request.user.is_god():
            self.request.messages.set_flash(Message(_('Role "%(name)s" is protected, you cannot edit it.') % {'name': _(result.name)}), 'error', self.admin.id)
            return None
        return result
    
    def submit_form(self, form, target):
        target.name = form.cleaned_data['name']
        if self.request.user.is_god():
            target.protected = form.cleaned_data['protected']
        target.save(force_update=True)
        self.request.monitor['acl_version'] = int(self.request.monitor['acl_version']) + 1
        return target, Message(_('Changes in role "%(name)s" have been saved.') % {'name': self.original_name}, 'success')


class Forums(ListWidget):
    admin = site.get_action('roles')
    id = 'forums'
    hide_actions = True
    name = _('Role Forums Permissions')
    table_form_button = _('Change Permissions')
    empty_message = _('No forums are currently defined.')
    template = 'forums'
    
    def get_url(self):
        return reverse('admin_roles_masks', self.role) 
    
    def get_items(self):
        return Forum.objects.get(token='root').get_descendants()
    
    def sort_items(self, page_items, sorting_method):
        return page_items.order_by('lft')

    def add_template_variables(self, variables):
        variables['target'] = _(self.role.name)
        return variables
    
    def get_table_form(self, page_items):
        perms = {}
        try:
            forums = self.role.get_permissions()['forums']
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
        print perms
        role_perms = self.role.get_permissions()
        role_perms['forums'] = perms
        self.role.set_permissions(role_perms)
        self.role.save(force_update=True)
        return Message(_('Forum permissions have been saved.'), 'success'), self.get_url()
        
    def __call__(self, request, slug, target):
        self.request = request
        try:
            self.role = Role.objects.get(id=target)
            if self.role and self.role.protected and not request.user.is_god():
                request.messages.set_flash(Message(_('Role "%(name)s" is protected, you cannot edit it.') % {'name': _(self.role.name)}), 'error', self.admin.id)
                return redirect(reverse('admin_roles'))
        except Role.DoesNotExist:
            request.set_flash(Message(_('Requested Role could not be found.')), 'error', self.admin.id)
            return redirect(reverse('admin_roles'))
        self.roles = ForumRole.objects.order_by('name').all()
        if not self.roles:
            request.set_flash(Message(_('No forum roles are currently set.')), 'error', self.admin.id)
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
    
    def get_url(self, model):
        return reverse('admin_roles_acl', model)
    
    def get_edit_url(self, model):
        return self.get_url(model)
    
    def get_initial_data(self, model):
        raw_acl = model.get_permissions()
        initial = {}
        for field in self.form.base_fields:
            if field in raw_acl:
                initial[field] = raw_acl[field]
        return initial
    
    def get_and_validate_target(self, target):
        result = super(ACL, self).get_and_validate_target(target)
        if result and result.protected and not self.request.user.is_god():
            self.request.messages.set_flash(Message(_('Role "%(name)s" is protected, you cannot edit it.') % {'name': _(result.name)}), 'error', self.admin.id)
            return None
        return result
    
    def submit_form(self, form, target):
        raw_acl = target.get_permissions()
        for perm in form.cleaned_data:
            raw_acl[perm] = form.cleaned_data[perm]
        target.set_permissions(raw_acl)
        target.save(force_update=True)
        self.request.monitor['acl_version'] = int(self.request.monitor['acl_version']) + 1
        
        return target, Message(_('Role "%(name)s" permissions have been changed.') % {'name': self.original_name}, 'success')


class Delete(ButtonWidget):
    admin = site.get_action('roles')
    id = 'delete'
    fallback = 'admin_roles'
    notfound_message = _('Requested Role could not be found.')
    
    def action(self, target):
        if target.token:
            return Message(_('You cannot delete system roles.'), 'error'), reverse('admin_roles')
        if target.protected and not self.request.user.is_god():
            return Message(_('This role is protected.'), 'error'), reverse('admin_roles')
        if target.user_set.count() > 0:
            return Message(_('This role is assigned to one or more users.'), 'error'), reverse('admin_roles')

        target.delete()
        return Message(_('Role "%(name)s" has been deleted.') % {'name': _(target.name)}, 'success'), False