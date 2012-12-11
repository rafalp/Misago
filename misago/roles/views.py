from django.core.urlresolvers import reverse as django_reverse
from django.utils.translation import ugettext as _
from misago.acl.builder import build_form 
from misago.admin import site
from misago.admin.widgets import *
from misago.utils import slugify
from misago.roles.forms import RoleForm, PermsForm
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
    
    def sort_items(self, request, page_items, sorting_method):
        return page_items.order_by('name')
    
    def get_item_actions(self, request, item):
        return (
                self.action('adjust', _("Role Permissions"), reverse('admin_roles_acl', item)),
                self.action('pencil', _("Edit Role"), reverse('admin_roles_edit', item)),
                self.action('remove', _("Delete Role"), reverse('admin_roles_delete', item), post=True, prompt=_("Are you sure you want to delete this role?")),
                )

    def action_delete(self, request, items, checked):
        for item in items:
            if unicode(item.pk) in checked:
                if item.token:
                    return Message(_('You cannot delete system roles.'), 'error'), reverse('admin_roles')
                if item.protected and not request.user.is_god():
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
        
    def get_new_url(self, request, model):
        return reverse('admin_roles_new')
    
    def get_edit_url(self, request, model):
        return reverse('admin_roles_edit', model)
    
    def submit_form(self, request, form, target):
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
    notfound_message = _('Requested Role could not be found.')
    submit_fallback = True
    
    def get_url(self, request, model):
        return reverse('admin_roles_edit', model)
    
    def get_edit_url(self, request, model):
        return self.get_url(request, model)
    
    def get_initial_data(self, request, model):
        return {
                'name': model.name,
                }
    
    def submit_form(self, request, form, target):
        target.name = form.cleaned_data['name']
        target.save(force_update=True)
        return target, Message(_('Changes in role "%(name)s" have been saved.') % {'name': self.original_name}, 'success')


class ACL(FormWidget):
    admin = site.get_action('roles')
    id = 'acl'
    name = _("Change Role Permissions")
    fallback = 'admin_roles'
    form = PermsForm
    target_name = 'name'
    notfound_message = _('Requested Role could not be found.')
    submit_fallback = True
    
    def get_form(self, request, target):
        self.form = build_form(request, self.form, target)
        return self.form
    
    def get_url(self, request, model):
        return reverse('admin_roles_acl', model)
    
    def get_edit_url(self, request, model):
        return self.get_url(request, model)
    
    def get_initial_data(self, request, model):
        raw_acl = model.get_permissions()
        initial = {}
        for field in self.form.base_fields:
            if field in raw_acl:
                initial[field] = raw_acl[field]
        return initial
    
    def submit_form(self, request, form, target):
        raw_acl = model.get_permissions()
        for perm in form.cleaned_data:
            raw_acl[perm] = form.cleaned_data[perm]
        target.set_permissions(raw_acl)
        target.save(force_update=True)
        request.model['acl_version'] = int(request.model['acl_version']) + 1
        
        return target, Message(_('Role "%(name)s" permissions have been changed.') % {'name': self.original_name}, 'success')


class Delete(ButtonWidget):
    admin = site.get_action('roles')
    id = 'delete'
    fallback = 'admin_roles'
    notfound_message = _('Requested Role could not be found.')
    
    def action(self, request, target):
        if target.token:
            return Message(_('You cannot delete system roles.'), 'error'), reverse('admin_roles')
        if target.protected and not request.user.is_god():
            return Message(_('This role is protected.'), 'error'), reverse('admin_roles')
        if target.user_set.count() > 0:
            return Message(_('This role is assigned to one or more usets.'), 'error'), reverse('admin_roles')

        target.delete()
        return Message(_('Role "%(name)s" has been deleted.') % {'name': target.name}, 'success'), False