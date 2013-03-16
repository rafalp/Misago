from django.core.urlresolvers import reverse as django_reverse
from django import forms
from django.utils.translation import ugettext as _
from misago.admin import site
from misago.admin.widgets import *
from misago.forms import Form
from misago.utils import slugify
from misago.themes.forms import ThemeAdjustmentForm
from misago.themes.models import ThemeAdjustment

def reverse(route, target=None):
    if target:
        return django_reverse(route, kwargs={'target': target.pk, 'slug': slugify(target.theme)})
    return django_reverse(route)

"""
Views
"""
class List(ListWidget):
    admin = site.get_action('clients')
    id = 'list'
    columns = (
               ('theme', _("Theme")),
               )
    nothing_checked_message = _('You have to check at least one adjustment.')
    actions = (
               ('delete', _("Delete selected adjustments"), _("Are you sure you want to delete selected theme adjustments?")),
               )

    def get_item_actions(self, item):
        return (
                self.action('pencil', _("Edit Adjustment"), reverse('admin_clients_edit', item)),
                self.action('remove', _("Delete Adjustment"), reverse('admin_clients_delete', item), post=True, prompt=_("Are you sure you want to delete this adjustment?")),
                )

    def action_delete(self, items, checked):
        ThemeAdjustment.objects.filter(id__in=checked).delete()
        return Message(_('Selected adjustment have been deleted successfully.'), 'success'), reverse('admin_clients')


class New(FormWidget):
    admin = site.get_action('clients')
    id = 'new'
    fallback = 'admin_clients'
    form = ThemeAdjustmentForm
    submit_button = _("Save Rank")

    def get_form_instance(self, form, model, initial, post=False):
        if post:
            return form(model, self.request.POST, request=self.request, initial=self.get_initial_data(model))
        return form(model, request=self.request, initial=self.get_initial_data(model))
    
    def get_new_url(self, model):
        return reverse('admin_clients_new')

    def get_edit_url(self, model):
        return reverse('admin_clients_edit', model)

    def submit_form(self, form, target):
        new_rank = ThemeAdjustment.objects.create(
                                                  theme=form.cleaned_data['theme'],
                                                  useragents='\r\n'.join(form.cleaned_data['useragents']),
                                                  )
        return new_rank, Message(_('New adjustment has been created.'), 'success')


class Edit(FormWidget):
    admin = site.get_action('clients')
    id = 'edit'
    name = _("Edit Rank")
    fallback = 'admin_clients'
    form = ThemeAdjustmentForm
    target_name = 'theme'
    notfound_message = _('Requested adjustment could not be found.')
    submit_fallback = True

    def get_url(self, model):
        return reverse('admin_clients_edit', model)

    def get_edit_url(self, model):
        return self.get_url(model)

    def get_form_instance(self, form, model, initial, post=False):
        if post:
            return form(model, self.request.POST, request=self.request, initial=self.get_initial_data(model))
        return form(model, request=self.request, initial=self.get_initial_data(model))
    
    def get_initial_data(self, model):
        return {
                'theme': model.theme,
                'useragents': model.useragents,
                }

    def submit_form(self, form, target):
        target.theme = form.cleaned_data['theme']
        target.useragents = '\r\n'.join(form.cleaned_data['useragents'])
        target.save(force_update=True)
        return target, Message(_('Adjustment using theme "%(name)s" has been saved.') % {'name': target.theme}, 'success')


class Delete(ButtonWidget):
    admin = site.get_action('clients')
    id = 'delete'
    fallback = 'admin_clients'
    notfound_message = _('Requested adjustment could not be found.')

    def action(self, target):
        target.delete()
        return Message(_('Adjustment using theme "%(name)s" has been deleted.') % {'name': target.theme}, 'success'), False
