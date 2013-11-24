from django.core.urlresolvers import reverse as django_reverse
from django.db.models import Q
from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago import messages
from misago.admin import site
from misago.apps.admin.widgets import *
from misago.messages import Message
from misago.models import Ban
from misago.monitor import monitor, UpdatingMonitor
from misago.apps.admin.bans.forms import BanForm, SearchBansForm

def reverse(route, target=None):
    if target:
        return django_reverse(route, kwargs={'target': target.pk})
    return django_reverse(route)


"""
Views
"""
class List(ListWidget):
    """
    List Bans
    """
    admin = site.get_action('bans')
    id = 'list'
    columns = (
             ('ban', _("Ban"), 50),
             ('expires', _("Expires")),
             )
    default_sorting = 'expires'
    sortables = {
               'ban': 1,
               'expires': 0,
              }
    pagination = 20
    search_form = SearchBansForm
    empty_message = _('No bans are currently set.')
    empty_search_message = _('No bans have been found.')
    nothing_checked_message = _('You have to check at least one ban.')
    actions = (
             ('delete', _("Lift selected bans"), _("Are you sure you want to lift selected bans?")),
             )

    def set_filters(self, model, filters):
        if 'ban' in filters:
            model = model.filter(ban__contains=filters['ban'])
        if 'reason' in filters:
            model = model.filter(Q(reason_user__contains=filters['reason']) | Q(reason_admin__contains=filters['reason']))
        if 'test' in filters:
            model = model.filter(test__in=filters['test'])
        return model

    def get_item_actions(self, item):
        return (
                self.action('pencil', _("Edit Ban"), reverse('admin_bans_edit', item)),
                self.action('remove', _("Lift Ban"), reverse('admin_bans_delete', item), post=True, prompt=_("Are you sure you want to lift this ban?")),
                )

    def action_delete(self, items, checked):
        Ban.objects.filter(id__in=checked).delete()
        with UpdatingMonitor() as cm:
            monitor.increase('bans_version')
        return Message(_('Selected bans have been lifted successfully.'), messages.SUCCESS), reverse('admin_bans')


class New(FormWidget):
    """
    Create Ban
    """
    admin = site.get_action('bans')
    id = 'new'
    fallback = 'admin_bans'
    form = BanForm
    submit_button = _("Set Ban")

    def get_new_link(self, model):
        return reverse('admin_bans_new')

    def get_edit_link(self, model):
        return reverse('admin_bans_edit', model)

    def submit_form(self, form, target):
        new_ban = Ban(
                      test=form.cleaned_data['test'],
                      ban=form.cleaned_data['ban'],
                      reason_user=form.cleaned_data['reason_user'],
                      reason_admin=form.cleaned_data['reason_admin'],
                      expires=form.cleaned_data['expires']
                     )
        new_ban.save(force_insert=True)
        with UpdatingMonitor() as cm:
            monitor.increase('bans_version')
        return new_ban, Message(_('New Ban has been set.'), messages.SUCCESS)


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

    def get_link(self, model):
        return reverse('admin_bans_edit', model)

    def get_edit_link(self, model):
        return self.get_link(model)

    def get_initial_data(self, model):
        return {
                'test': model.test,
                'ban': model.ban,
                'reason_user': model.reason_user,
                'reason_admin': model.reason_admin,
                'expires': model.expires,
                }

    def submit_form(self, form, target):
        target.test = form.cleaned_data['test']
        target.ban = form.cleaned_data['ban']
        target.reason_user = form.cleaned_data['reason_user']
        target.reason_admin = form.cleaned_data['reason_admin']
        target.expires = form.cleaned_data['expires']
        target.save(force_update=True)
        with UpdatingMonitor() as cm:
            monitor.increase('bans_version')
        return target, Message(_('Changes in ban have been saved.'), messages.SUCCESS)


class Delete(ButtonWidget):
    """
    Delete Ban
    """
    admin = site.get_action('bans')
    id = 'delete'
    fallback = 'admin_bans'
    notfound_message = _('Requested Ban could not be found.')

    def action(self, target):
        target.delete()
        with UpdatingMonitor() as cm:
            monitor.increase('bans_version')
        if target.test == 0:
            return Message(_('E-mail and username Ban "%(ban)s" has been lifted.') % {'ban': target.ban}, messages.SUCCESS), False
        if target.test == 1:
            return Message(_('Username Ban "%(ban)s" has been lifted.') % {'ban': target.ban}, messages.SUCCESS), False
        if target.test == 2:
            return Message(_('E-mail Ban "%(ban)s" has been lifted.') % {'ban': target.ban}, messages.SUCCESS), False
        if target.test == 3:
            return Message(_('IP Ban "%(ban)s" has been lifted.') % {'ban': target.ban}, messages.SUCCESS), False
