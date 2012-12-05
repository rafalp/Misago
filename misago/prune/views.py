from django.core.urlresolvers import reverse as django_reverse
from django import forms
from django.utils.translation import ugettext as _
from misago.admin import site
from misago.admin.widgets import *
from misago.forms import Form
from misago.prune.forms import PolicyForm
from misago.prune.models import Policy

def reverse(route, target=None):
    if target:
        return django_reverse(route, kwargs={'target': target.pk})
    return django_reverse(route)

"""
Views
"""
class List(ListWidget):
    admin = site.get_action('prune_users')
    id = 'list'
    columns=(
             ('name', _("Pruning Policy")),
             )
    nothing_checked_message = _('You have to check at least one policy.')
    actions=(
             ('delete', _("Delete selected policies"), _("Are you sure you want to delete selected policies?")),
             )
    
    def sort_items(self, request, page_items, sorting_method):
        return page_items.order_by('name')
    
    def get_item_actions(self, request, item):
        return (
                self.action('pencil', _("Edit Pruning Policy"), reverse('admin_pruning_edit', item)),
                self.action('remove', _("Delete Pruning Policy"), reverse('admin_pruning_delete', item), post=True, prompt=_("Are you sure you want to delete this rank?")),
                )

    def action_delete(self, request, items, checked):
        if not request.user.is_god():
            return Message(_('Only system administrators can delete pruning policies.'), 'error'), reverse('admin_prune_users')
        
        Policy.objects.filter(id__in=checked).delete()
        return Message(_('Selected pruning policies have been deleted successfully.'), 'success'), reverse('admin_prune_users')


class New(FormWidget):
    admin = site.get_action('prune_users')
    id = 'new'
    fallback = 'admin_prune_users' 
    form = PolicyForm
    submit_button = _("Save Policy")
        
    def get_new_url(self, request, model):
        return reverse('admin_prune_users')
    
    def get_edit_url(self, request, model):
        return reverse('admin_pruning_edit', model)
    
    def submit_form(self, request, form, target):
        new_policy = Policy(
                      name = form.cleaned_data['name'],
                      email = form.cleaned_data['email'],
                      posts = form.cleaned_data['posts'],
                      registered = form.cleaned_data['registered'],
                      last_visit = form.cleaned_data['last_visit'],
                     )
        new_policy.save(force_insert=True)
        
        return new_policy, Message(_('New Pruning Policy has been created.'), 'success')
    
    def __call__(self, request, *args, **kwargs):
        if not request.user.is_god():
            request.messages.set_flash(Message(_('Only system administrators can set new pruning policies.')), 'error', self.admin.id)
            return redirect(reverse('admin_prune_users'))
        
        return super(New, self).__call__(request, *args, **kwargs)

  
class Edit(FormWidget):
    admin = site.get_action('prune_users')
    id = 'edit'
    name = _("Edit Pruning Policy")
    fallback = 'admin_prune_users'
    form = PolicyForm
    target_name = 'name'
    notfound_message = _('Requested pruning policy could not be found.')
    submit_fallback = True
    
    def get_url(self, request, model):
        return reverse('admin_pruning_edit', model)
    
    def get_edit_url(self, request, model):
        return self.get_url(request, model)
    
    def get_initial_data(self, request, model):
        return {
                'name': model.name,
                'email': model.email,
                'posts': model.posts,
                'registered': model.registered,
                'last_visit': model.last_visit,
                }
    
    def submit_form(self, request, form, target):
        target.name = form.cleaned_data['name']
        target.email = form.cleaned_data['email']
        target.posts = form.cleaned_data['posts']
        target.registered = form.cleaned_data['registered']
        target.last_visit = form.cleaned_data['last_visit']
        target.save(force_update=True)
        
        return target, Message(_('Changes in policy "%(name)s" have been saved.') % {'name': self.original_name}, 'success')
    
    def __call__(self, request, *args, **kwargs):
        if not request.user.is_god():
            request.messages.set_flash(Message(_('Only system administrators can edit pruning policies.')), 'error', self.admin.id)
            return redirect(reverse('admin_prune_users'))
        
        return super(Edit, self).__call__(request, *args, **kwargs)


class Delete(ButtonWidget):
    admin = site.get_action('prune_users')
    id = 'delete'
    fallback = 'admin_prune_users'
    notfound_message = _('Requested pruning policy could not be found.')
    
    def action(self, request, target):
        if not request.user.is_god():
            return Message(_('Only system administrators can delete pruning policies.'), 'error'), False
        
        target.delete()
        return Message(_('Pruning policy "%(name)s" has been deleted.') % {'name': target.name}, 'success'), False