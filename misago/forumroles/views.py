import copy
from django.core.urlresolvers import reverse as django_reverse
from django.utils.translation import ugettext as _
from misago.acl.builder import build_forum_form 
from misago.admin import site
from misago.admin.widgets import *
from misago.utils import slugify
from misago.forms import Form, YesNoSwitch
from misago.forumroles.forms import ForumRoleForm
from misago.forumroles.models import ForumRole

def reverse(route, target=None):
    if target:
        return django_reverse(route, kwargs={'target': target.pk, 'slug': slugify(target.name)})
    return django_reverse(route)

"""
Views
"""
class List(ListWidget):
    admin = site.get_action('roles_forums')
    id = 'list'
    columns=(
             ('role', _("Role")),
             )
    nothing_checked_message = _('You have to check at least one role.')
    actions=(
             ('delete', _("Delete selected forum roles"), _("Are you sure you want to delete selected roles?")),
             )
    
    def sort_items(self, request, page_items, sorting_method):
        return page_items.order_by('name')
    
    def get_item_actions(self, request, item):
        return (
                self.action('adjust', _("Role Permissions"), reverse('admin_roles_forums_acl', item)),
                self.action('pencil', _("Edit Role"), reverse('admin_roles_forums_edit', item)),
                self.action('remove', _("Delete Role"), reverse('admin_roles_forums_delete', item), post=True, prompt=_("Are you sure you want to delete this role?")),
                )

    def action_delete(self, request, items, checked):
        request.monitor['acl_version'] = int(request.monitor['acl_version']) + 1
        Role.objects.filter(id__in=checked).delete()
        return Message(_('Selected forum roles have been deleted successfully.'), 'success'), reverse('admin_roles_forums')


class New(FormWidget):
    admin = site.get_action('roles_forums')
    id = 'new'
    fallback = 'admin_roles_forums' 
    form = ForumRoleForm
    submit_button = _("Save Role")
        
    def get_new_url(self, request, model):
        return reverse('admin_roles_forums_new')
    
    def get_edit_url(self, request, model):
        return reverse('admin_roles_forums_edit', model)
    
    def submit_form(self, request, form, target):
        new_role = ForumRole(
                      name = form.cleaned_data['name'],
                     )
        new_role.save(force_insert=True)
        return new_role, Message(_('New Forum Role has been created.'), 'success')
    
   
class Edit(FormWidget):
    admin = site.get_action('roles_forums')
    id = 'edit'
    name = _("Edit Forum Role")
    fallback = 'admin_roles_forums'
    form = ForumRoleForm
    target_name = 'name'
    notfound_message = _('Requested Forum Role could not be found.')
    submit_fallback = True
    
    def get_url(self, request, model):
        return reverse('admin_roles_forums_edit', model)
    
    def get_edit_url(self, request, model):
        return self.get_url(request, model)
    
    def get_initial_data(self, request, model):
        return {
                'name': model.name,
                }
    
    def submit_form(self, request, form, target):
        target.name = form.cleaned_data['name']
        target.save(force_update=True)
        return target, Message(_('Changes in forum role "%(name)s" have been saved.') % {'name': self.original_name}, 'success')


class ACL(FormWidget):
    admin = site.get_action('roles_forums')
    id = 'acl'
    name = _("Change Forum Role Permissions")
    fallback = 'admin_roles_forums'
    target_name = 'name'
    notfound_message = _('Requested Forum Role could not be found.')
    submit_fallback = True
    template = 'acl_form'
    
    def get_form(self, request, target):
        self.form = build_forum_form(request, target)
        return self.form
    
    def get_url(self, request, model):
        return reverse('admin_roles_forums_acl', model)
    
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
        raw_acl = target.get_permissions()
        for perm in form.cleaned_data:
            raw_acl[perm] = form.cleaned_data[perm]
        target.set_permissions(raw_acl)
        target.save(force_update=True)
        request.monitor['acl_version'] = int(request.monitor['acl_version']) + 1
        
        return target, Message(_('Forum Role "%(name)s" permissions have been changed.') % {'name': self.original_name}, 'success')


class Delete(ButtonWidget):
    admin = site.get_action('roles_forums')
    id = 'delete'
    fallback = 'admin_roles_forums'
    notfound_message = _('Requested Forum Role could not be found.')
    
    def action(self, request, target):
        target.delete()
        request.monitor['acl_version'] = int(request.monitor['acl_version']) + 1
        return Message(_('Forum Role "%(name)s" has been deleted.') % {'name': _(target.name)}, 'success'), False