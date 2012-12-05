from django.core.urlresolvers import reverse as django_reverse
from django.db.models import Q
from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago.admin import site
from misago.admin.widgets import *
from misago.banning.forms import BanForm, SearchBansForm
from misago.banning.models import Ban
from misago.messages import Message

"""
Admin mixin
"""
def reverse(route, target=None):
    if target:
        return django_reverse(route, kwargs={'target': target.pk})
    return django_reverse(route)

"""
Views
"""
def error_banned(request, user=None, ban=None):
    if not ban:
        ban = request.ban
    response = request.theme.render_to_response('error403_banned.html',
                                                {
                                                 'banned_user': user,
                                                 'ban': ban,
                                                 'hide_signin': True,
                                                 'exception_response': True,
                                                 },
                                                context_instance=RequestContext(request));
    response.status_code = 403
    return response


class List(ListWidget):
    """
    List Bans
    """
    admin = site.get_action('bans')
    id = 'list'
    columns=(
             ('ban', _("Ban"), 50),
             ('expires', _("Expires")),
             )
    default_sorting = 'expires'
    sortables={
               'ban': 1,
               'expires': 0,
              }
    pagination = 20
    search_form = SearchBansForm
    empty_message = _('No bans are currently set.')
    empty_search_message = _('No bans have been found.')
    nothing_checked_message = _('You have to check at least one ban.')
    actions=(
             ('delete', _("Lift selected bans"), _("Are you sure you want to lift selected bans?")),
             )
    
    def set_filters(self, model, filters):
        if 'ban' in filters:
            model = model.filter(ban__contains=filters['ban'])
        if 'reason' in filters:
            model = model.filter(Q(reason_user__contains=filters['reason']) | Q(reason_admin__contains=filters['reason']))
        if 'type' in filters:
            model = model.filter(type__in=filters['type'])
        return model
    
    def get_item_actions(self, request, item):
        return (
                self.action('pencil', _("Edit Ban"), reverse('admin_bans_edit', item)),
                self.action('remove', _("Lift Ban"), reverse('admin_bans_delete', item), post=True, prompt=_("Are you sure you want to lift this ban?")),
                )

    def action_delete(self, request, items, checked):
        Ban.objects.filter(id__in=checked).delete()
        request.monitor['bans_version'] = int(request.monitor['bans_version']) + 1
        return Message(_('Selected bans have been lifted successfully.'), 'success'), reverse('admin_bans')
    

class New(FormWidget):
    """
    Create Ban
    """
    admin = site.get_action('bans')
    id = 'new'
    fallback = 'admin_bans' 
    form = BanForm
    submit_button = _("Set Ban")
        
    def get_new_url(self, request, model):
        return reverse('admin_bans')
    
    def get_edit_url(self, request, model):
        return reverse('admin_bans_edit', model)
    
    def submit_form(self, request, form, target):
        new_ban = Ban(
                      type = form.cleaned_data['type'],
                      ban = form.cleaned_data['ban'],
                      reason_user = form.cleaned_data['reason_user'],
                      reason_admin = form.cleaned_data['reason_admin'],
                      expires = form.cleaned_data['expires']
                     )
        new_ban.save(force_insert=True)
        request.monitor['bans_version'] = int(request.monitor['bans_version']) + 1
        return new_ban, Message(_('New Ban has been set.'), 'success')
    
   
class Edit(FormWidget):
    """
    Edit Ban
    """
    admin = site.get_action('bans')
    id = 'edit'
    name = _("Edit Ban")
    fallback = 'admin_bans'
    form = BanForm
    target_name = 'ban'
    notfound_message = _('Requested Ban could not be found.')
    submit_fallback = True
    
    def get_url(self, request, model):
        return reverse('admin_bans_edit', model)
    
    def get_edit_url(self, request, model):
        return self.get_url(request, model)
    
    def get_initial_data(self, request, model):
        return {
                'type': model.type,
                'ban': model.ban,
                'reason_user': model.reason_user,
                'reason_admin': model.reason_admin,
                'expires': model.expires,
                }
    
    def submit_form(self, request, form, target):
        target.type = form.cleaned_data['type']
        target.ban = form.cleaned_data['ban']
        target.reason_user = form.cleaned_data['reason_user']
        target.reason_admin = form.cleaned_data['reason_admin']
        target.expires = form.cleaned_data['expires']
        target.save(force_update=True)
        request.monitor['bans_version'] = int(request.monitor['bans_version']) + 1
        return target, Message(_('Changes in ban have been saved.'), 'success')


class Delete(ButtonWidget):
    """
    Delete Ban
    """
    admin = site.get_action('bans')
    id = 'delete'
    fallback = 'admin_bans'
    notfound_message = _('Requested Ban could not be found.')
    
    def action(self, request, target):
        target.delete()
        request.monitor['bans_version'] = int(request.monitor['bans_version']) + 1
        if target.type == 0:
            return Message(_('E-mail and username Ban "%(ban)s" has been lifted.') % {'ban': target.ban}, 'success'), False
        if target.type == 1:
            return Message(_('Username Ban "%(ban)s" has been lifted.') % {'ban': target.ban}, 'success'), False
        if target.type == 2:
            return Message(_('E-mail Ban "%(ban)s" has been lifted.') % {'ban': target.ban}, 'success'), False
        if target.type == 3:
            return Message(_('IP Ban "%(ban)s" has been lifted.') % {'ban': target.ban}, 'success'), False
        
        