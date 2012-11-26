from django.core.urlresolvers import reverse as django_reverse
from django.utils.translation import ugettext as _
from misago.admin import site
from misago.admin.widgets import *
from misago.utils import slugify
from misago.users.admin.users.forms import UserForm, SearchUsersForm
from misago.users.models import User

def reverse(route, target=None):
    if target:
        return django_reverse(route, kwargs={'target': target.pk, 'slug': target.username_slug})
    return django_reverse(route)

"""
Views
"""
class List(ListWidget):
    admin = site.get_action('users')
    id = 'list'
    columns=(
             ('username_slug', _("User Name"), 35),
             ('join_date', _("Join Date")),
             )
    default_sorting = 'username'
    sortables={
               'username_slug': 1,
               'join_date': 0,
              }
    pagination = 25
    search_form = SearchUsersForm
    nothing_checked_message = _('You have to check at least one user.')
    actions=(
             ('reset', _("Reset passwords"), _("Are you sure you want to reset selected members passwords?")),
             ('remove_avs', _("Remove avatars"), _("Are you sure you want to reset selected members passwords?")),
             ('delete', _("Delete selected"), _("Are you sure you want to delete selected users?")),
             )
    
    def set_filters(self, model, filters):
        if 'role' in filters:
            model = model.filter(roles__in=filters['role']).distinct()
        if 'rank' in filters:
            model = model.filter(rank__in=filters['rank'])
        if 'username' in filters:
            model = model.filter(username_slug__contains=filters['username'])
        if 'email' in filters:
            model = model.filter(email__contains=filters['email'])
        if 'activation' in filters:
            model = model.filter(activation__in=filters['activation'])
        return model
    
    def prefetch_related(self, items):
        return items.prefetch_related('roles')
    
    def get_item_actions(self, request, item):
        return (
                self.action('pencil', _("Edit User Details"), reverse('admin_users_edit', item)),
                self.action('remove', _("Delete User"), reverse('admin_users_delete', item), post=True, prompt=_("Are you sure you want to delete this user account?")),
                )

    def action_delete(self, request, items, checked):
        for user in items:
            if unicode(user.pk) in checked:
                if user.pk == request.user.id:
                    return BasicMessage(_('You cannot delete yourself.'), 'error'), reverse('admin_users')
                if user.is_protected():
                    return BasicMessage(_('You cannot delete protected member.'), 'error'), reverse('admin_users')
                
        User.objects.filter(id__in=checked).delete()
        User.objects.resync_monitor(request.monitor)
        return BasicMessage(_('Selected users have been deleted successfully.'), 'success'), reverse('admin_users')
    

class Edit(FormWidget):
    admin = site.get_action('users')
    id = 'edit'
    name = _("Edit User")
    fallback = 'admin_users'
    form = UserForm
    target_name = 'username'
    notfound_message = _('Requested User could not be found.')
    submit_fallback = True
    
    def get_form_instance(self, form, request, model, initial, post=False):
        if post:
            return form(model, request.POST, request=request, initial=self.get_initial_data(request, model))
        return form(model, request=request, initial=self.get_initial_data(request, model))
        
    def get_url(self, request, model):
        return reverse('admin_users_edit', model)
    
    def get_edit_url(self, request, model):
        return self.get_url(request, model)
    
    def get_initial_data(self, request, model):
        return {
                'username': model.username,
                'title': model.title,
                'email': model.email,
                'rank': model.rank,
                'roles': model.roles.all(),
                }
    
    def submit_form(self, request, form, target):
        target.title = form.cleaned_data['title']
        target.rank = form.cleaned_data['rank']
        if not target.is_protected() or request.user.is_god():
            target.roles.clear()
            for role in form.cleaned_data['roles']:
                target.roles.add(role)
        target.save(force_update=True)
        return target, BasicMessage(_('Changes in user\'s "%(name)s" account have been saved.' % {'name': self.original_name}), 'success')


class Delete(ButtonWidget):
    admin = site.get_action('users')
    id = 'delete'
    fallback = 'admin_users'
    notfound_message = _('Requested user account could not be found.')
    
    def action(self, request, target):
        if target.pk == request.user.id:
            return BasicMessage(_('You cannot delete yourself.'), 'error'), False
        if target.is_protected():
            return BasicMessage(_('You cannot delete protected member.'), 'error'), False
        target.delete()
        User.objects.resync_monitor(request.monitor)
        return BasicMessage(_('User "%(name)s" has been deleted.' % {'name': target.username}), 'success'), False
    

def inactive(request):
    token = 'list_filter_misago.users.models.User'
    request.session[token] = {'activation': ['1', '2', '3']}
    return redirect(reverse('admin_users'))