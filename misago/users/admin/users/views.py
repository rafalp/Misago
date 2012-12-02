from django.core.urlresolvers import reverse as django_reverse
from django.db.models import Q
from django.utils.translation import ugettext as _
from misago.admin import site
from misago.admin.widgets import *
from misago.security import get_random_string
from misago.utils import slugify
from misago.users.admin.users.forms import UserForm, NewUserForm, SearchUsersForm
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
             ('activate', _("Activate users"), _("Are you sure you want to activate selected members?")),
             ('deactivate', _("Request e-mail validation"), _("Are you sure you want to deactivate selected members and request them to revalidate their e-mail addresses?")),
             ('remove_av', _("Remove and lock avatars"), _("Are you sure you want to remove selected members avatars and their ability to change them?")),
             ('remove_sig', _("Remove and lock signatures"), _("Are you sure you want to remove selected members signatures and their ability to edit them?")),
             ('remove_locks', _("Remove locks from avatars and signatures"), _("Are you sure you want to remove locks from selected members avatars and signatures?")),
             ('reset', _("Reset passwords"), _("Are you sure you want to reset selected members passwords?")),
             ('delete', _("Delete users"), _("Are you sure you want to delete selected users?")),
             )
    
    def set_filters(self, model, filters):
        if 'role' in filters:
            model = model.filter(roles__in=filters['role']).distinct()
        if 'rank' in filters:
            model = model.filter(rank__in=filters['rank'])
        if 'username' in filters:
            if ',' in filters['username']:
                qs = None
                for name in filters['username'].split(','):
                    name = name.strip().lower()
                    if name:
                        if qs:
                            qs = qs | Q(username_slug__contains=name)
                        else:
                            qs = Q(username_slug__contains=name)
                if qs:
                    model = model.filter(qs)
            else:
                model = model.filter(username_slug__contains=filters['username'])
        if 'email' in filters:
            if ',' in filters['email']:
                qs = None
                for name in filters['email'].split(','):
                    name = name.strip().lower()
                    if name:
                        if qs:
                            qs = qs | Q(email__contains=name)
                        else:
                            qs = Q(email__contains=name)
                if qs:
                    model = model.filter(qs)
            else:
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
    
    def action_activate(self, request, items, checked):
        for user in items:
            if unicode(user.pk) in checked and user.activation > 0:
                request.monitor['users_inactive'] = int(request.monitor['users_inactive']) - 1
                user.activation = user.ACTIVATION_NONE
                user.save(force_update=True)
                user.email_user(
                                request,
                                'users/activation/admin_done',
                                _("Your Account has been activated"),
                                )
                
        return Message(_('Selected users accounts have been activated.'), 'success'), reverse('admin_users')
    
    def action_deactivate(self, request, items, checked):
        # First loop - check for errors
        for user in items:
            if unicode(user.pk) in checked:
                if user.is_protected() and not request.user.is_god():
                    return Message(_('You cannot force validation of protected members e-mails.'), 'error'), reverse('admin_users')
                
        # Second loop - reset passwords
        for user in items:
            if unicode(user.pk) in checked:
                user.activation = user.ACTIVATION_USER
                user.token = token = get_random_string(12)
                user.save(force_update=True)
                user.email_user(
                                request,
                                'users/activation/invalidated',
                                _("Account Activation"),
                                )
                
        return Message(_('Selected users accounts have been deactivated and new activation links have been sent to them.'), 'success'), reverse('admin_users')

    def action_remove_av(self, request, items, checked):
        # First loop - check for errors
        for user in items:
            if unicode(user.pk) in checked:
                if user.is_protected() and not request.user.is_god():
                    return Message(_('You cannot remove and block protected members avatars.'), 'error'), reverse('admin_users')
                
        # Second loop - reset passwords
        for user in items:
            if unicode(user.pk) in checked:
                user.lock_avatar()
                user.save(force_update=True)
                
        return Message(_('Selected users avatars were deleted and locked.'), 'success'), reverse('admin_users')

    def action_remove_sig(self, request, items, checked):
        # First loop - check for errors
        for user in items:
            if unicode(user.pk) in checked:
                if user.is_protected() and not request.user.is_god():
                    return Message(_('You cannot remove and block protected members signatures.'), 'error'), reverse('admin_users')
                
        # Second loop - reset passwords
        for user in items:
            if unicode(user.pk) in checked:
                user.signature_ban = True
                user.signature = ''
                user.signature_preparsed = ''
                user.save(force_update=True)
                
        return Message(_('Selected users signatures were deleted and locked.'), 'success'), reverse('admin_users')
   
    def action_remove_locks(self, request, items, checked):
        for user in items:
            if unicode(user.pk) in checked:
                user.default_avatar(request.settings)
                user.avatar_ban = False
                user.signature_ban = False
                user.save(force_update=True)
                
        return Message(_('Selected users can now edit their avatars and signatures.'), 'success'), reverse('admin_users')
    
    def action_reset(self, request, items, checked):
        # First loop - check for errors
        for user in items:
            if unicode(user.pk) in checked:
                if user.is_protected() and not request.user.is_god():
                    return Message(_('You cannot reset protected members passwords.'), 'error'), reverse('admin_users')
                
        # Second loop - reset passwords
        for user in items:
            if unicode(user.pk) in checked:
                new_password = get_random_string(8)
                user.set_password(new_password)
                user.save(force_update=True)
                user.email_user(
                                request,
                                'users/password/new_admin',
                                _("Your New Password"),
                                {
                                 'password': new_password,
                                 },
                                )
                
        return Message(_('Selected users passwords have been reset successfully.'), 'success'), reverse('admin_users')

    def action_delete(self, request, items, checked):
        for user in items:
            if unicode(user.pk) in checked:
                if user.pk == request.user.id:
                    return Message(_('You cannot delete yourself.'), 'error'), reverse('admin_users')
                if user.is_protected():
                    return Message(_('You cannot delete protected members.'), 'error'), reverse('admin_users')
                
        User.objects.filter(id__in=checked).delete()
        User.objects.resync_monitor(request.monitor)
        return Message(_('Selected users have been deleted successfully.'), 'success'), reverse('admin_users')
    

class New(FormWidget):
    admin = site.get_action('users')
    id = 'new'
    fallback = 'admin_users' 
    form = NewUserForm
    submit_button = _("Save User")
        
    def get_new_url(self, request, model):
        return reverse('admin_users')
    
    def get_edit_url(self, request, model):
        return reverse('admin_users_edit', model)
    
    def submit_form(self, request, form, target):
        new_user = User.objects.create_user(
                                            form.cleaned_data['username'],
                                            form.cleaned_data['email'],
                                            form.cleaned_data['password'],
                                            request.settings['default_timezone'],
                                            request.META['REMOTE_ADDR'],
                                            no_roles=True,
                                            request=request,
                                            )
        new_user.title = form.cleaned_data['title']
        new_user.rank = form.cleaned_data['rank']
        
        for role in form.cleaned_data['roles']:
            new_user.roles.add(role)
        new_user.save(force_update=True)
        
        return new_user, Message(_('New User has been created.'), 'success')
    
    
class Edit(FormWidget):
    admin = site.get_action('users')
    id = 'edit'
    name = _("Edit User")
    fallback = 'admin_users'
    form = UserForm
    tabbed = True
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
                'avatar_ban': model.avatar_ban,
                'avatar_ban_reason_user': model.avatar_ban_reason_user,
                'avatar_ban_reason_admin': model.avatar_ban_reason_admin,
                'signature': model.signature,
                'signature_ban': model.signature_ban,
                'signature_ban_reason_user': model.signature_ban_reason_user,
                'signature_ban_reason_admin': model.signature_ban_reason_admin,
                }
    
    def submit_form(self, request, form, target):
        target.title = form.cleaned_data['title']
        target.rank = form.cleaned_data['rank']
        target.avatar_ban_reason_user = form.cleaned_data['avatar_ban_reason_user']
        target.avatar_ban_reason_admin = form.cleaned_data['avatar_ban_reason_admin']
        target.set_signature(form.cleaned_data['signature'])
        target.signature_ban = form.cleaned_data['signature_ban']
        target.signature_ban_reason_user = form.cleaned_data['signature_ban_reason_user']
        target.signature_ban_reason_admin = form.cleaned_data['signature_ban_reason_admin']
        
        # Do avatar ban mumbo-jumbo
        if target.avatar_ban != form.cleaned_data['avatar_ban']:
            if form.cleaned_data['avatar_ban']:
                target.lock_avatar()
            else:
                target.default_avatar(request.settings)
        target.avatar_ban = form.cleaned_data['avatar_ban']
               
        # Set custom avatar
        if form.cleaned_data['avatar_custom']:
            target.delete_avatar()
            target.avatar_image = form.cleaned_data['avatar_custom']
            target.avatar_type = 'gallery'
        
        # Update user roles
        if request.user.is_god():
            target.roles.clear()
            for role in form.cleaned_data['roles']:
                target.roles.add(role)
        else:
            for role in target.roles.all():
                if not role.protected:
                    target.roles.remove(role)
            for role in form.cleaned_data['roles']:
                target.roles.add(role)
        
        target.save(force_update=True)
        return target, Message(_('Changes in user\'s "%(name)s" account have been saved.') % {'name': self.original_name}, 'success')


class Delete(ButtonWidget):
    admin = site.get_action('users')
    id = 'delete'
    fallback = 'admin_users'
    notfound_message = _('Requested user account could not be found.')
    
    def action(self, request, target):
        if target.pk == request.user.id:
            return Message(_('You cannot delete yourself.'), 'error'), False
        if target.is_protected():
            return Message(_('You cannot delete protected member.'), 'error'), False
        target.delete()
        User.objects.resync_monitor(request.monitor)
        return Message(_('User "%(name)s" has been deleted.') % {'name': target.username}, 'success'), False
    

def inactive(request):
    token = 'list_filter_misago.users.models.User'
    request.session[token] = {'activation': ['1', '2', '3']}
    return redirect(reverse('admin_users'))