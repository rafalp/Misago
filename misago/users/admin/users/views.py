from django.core.urlresolvers import reverse as django_reverse
from django.utils.translation import ugettext as _
from misago.admin import site
from misago.admin.widgets import *
from misago.utils import slugify
from misago.users.admin.users.forms import SearchUsersForm
from misago.users.models import User

def reverse(route, target=None):
    if target:
        return django_reverse(route, kwargs={'target': target.pk, 'slug': slugify(target.username)})
    return django_reverse(route)

"""
Views
"""
class List(ListWidget):
    """
    List Users
    """
    admin = site.get_action('users')
    id = 'list'
    columns=(
             ('username_slug', _("User Name"), 50),
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
        if 'username' in filters:
            model = model.filter(username_slug__contains=filters['username'])
        if 'email' in filters:
            model = model.filter(email__contains=filters['email'])
        if 'activation' in filters:
            model = model.filter(activation__in=filters['activation'])
        return model
    
    def get_item_actions(self, request, item):
        return (
                self.action('pencil', _("Edit User Details"), reverse('admin_qa_edit', item)),
                self.action('remove', _("Delete User"), reverse('admin_users_delete', item), post=True, prompt=_("Are you sure you want to delete this user account?")),
                )

    def action_delete(self, request, items, checked):
        print '%r' % checked
        for user in items:
            if unicode(user.pk) in checked:
                if user.pk == request.user.id:
                    return BasicMessage(_('You cannot delete yourself.'), 'error'), reverse('admin_users')
                if user.is_god():
                    return BasicMessage(_('You cannot delete system administrator.'), 'error'), reverse('admin_users')
                
        User.objects.filter(id__in=checked).delete()
        User.objects.resync_monitor(request.monitor)
        return BasicMessage(_('Selected users have been deleted successfully.'), 'success'), reverse('admin_users')


class Delete(ButtonWidget):
    """
    Delete QA Test
    """
    admin = site.get_action('users')
    id = 'delete'
    fallback = 'admin_users'
    notfound_message = _('Requested user account could not be found.')
    
    def action(self, request, target):
        if target.pk == request.user.id:
            return BasicMessage(_('You cannot delete yourself.'), 'error'), False
        if target.is_god():
            return BasicMessage(_('You cannot delete system administrator.'), 'error'), False
        target.delete()
        User.objects.resync_monitor(request.monitor)
        return BasicMessage(_('User "%(name)s" has been deleted.' % {'name': target.username}), 'success'), False