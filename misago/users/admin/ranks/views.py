from django.core.urlresolvers import reverse as django_reverse
from django import forms
from django.utils.translation import ugettext as _
from misago.admin import site
from misago.admin.widgets import *
from misago.forms import Form
from misago.utils import slugify
from misago.users.admin.ranks.forms import RankForm
from misago.users.models import Rank

def reverse(route, target=None):
    if target:
        return django_reverse(route, kwargs={'target': target.pk, 'slug': slugify(target.name)})
    return django_reverse(route)

"""
Views
"""
class List(ListWidget):
    admin = site.get_action('ranks')
    id = 'list'
    columns=(
             ('rank', _("Rank")),
             )
    table_form_button = _('Reorder Ranks')
    nothing_checked_message = _('You have to check at least one rank.')
    actions=(
             ('delete', _("Delete selected ranks"), _("Are you sure you want to delete selected ranks?")),
             )
    
    
    def get_table_form(self, request, page_items):
        order_form = {}
        
        # Build choices list
        choices = []
        for i in range(0, len(page_items)):
           choices.append([str(i), i + 1])
        
        # Build selectors list
        position = 0
        for item in page_items:
            order_form['pos_' + str(item.pk)] = forms.ChoiceField(choices=choices,initial=str(position))
            position += 1
        
        # Turn dict into object
        return type('OrderRanksForm', (Form,), order_form)
    
    def table_action(self, request, page_items, cleaned_data):
        for item in page_items:
            item.order = cleaned_data['pos_' + str(item.pk)]
            item.save(force_update=True)
        return Message(_('Ranks order has been changed'), 'success'), reverse('admin_users_ranks')
    
    def sort_items(self, request, page_items, sorting_method):
        return page_items.order_by('order')
    
    def get_item_actions(self, request, item):
        return (
                self.action('pencil', _("Edit Rank"), reverse('admin_users_ranks_edit', item)),
                self.action('remove', _("Delete Rank"), reverse('admin_users_ranks_delete', item), post=True, prompt=_("Are you sure you want to delete this rank?")),
                )

    def action_delete(self, request, items, checked):
        Rank.objects.filter(id__in=checked).delete()
        return Message(_('Selected ranks have been deleted successfully.'), 'success'), reverse('admin_users_ranks')


class New(FormWidget):
    admin = site.get_action('ranks')
    id = 'new'
    fallback = 'admin_users_ranks' 
    form = RankForm
    submit_button = _("Save Rank")
        
    def get_new_url(self, request, model):
        return reverse('admin_users_ranks')
    
    def get_edit_url(self, request, model):
        return reverse('admin_users_ranks_edit', model)
    
    def submit_form(self, request, form, target):
        position = 0
        last_rank = Rank.objects.latest('order')
        new_rank = Rank(
                      name = form.cleaned_data['name'],
                      name_slug = slugify(form.cleaned_data['name']),
                      description = form.cleaned_data['description'],
                      style = form.cleaned_data['style'],
                      title = form.cleaned_data['title'],
                      special = form.cleaned_data['special'],
                      as_tab = form.cleaned_data['as_tab'],
                      order = (last_rank.order + 1 if last_rank else 0),
                      criteria = form.cleaned_data['criteria']
                     )
        new_rank.save(force_insert=True)
        return new_rank, Message(_('New Rank has been created.'), 'success')
    
   
class Edit(FormWidget):
    admin = site.get_action('ranks')
    id = 'edit'
    name = _("Edit Rank")
    fallback = 'admin_users_ranks'
    form = RankForm
    target_name = 'name'
    notfound_message = _('Requested Rank could not be found.')
    submit_fallback = True
    
    def get_url(self, request, model):
        return reverse('admin_users_ranks_edit', model)
    
    def get_edit_url(self, request, model):
        return self.get_url(request, model)
    
    def get_initial_data(self, request, model):
        return {
                'name': model.name,
                'description': model.description,
                'style': model.style,
                'title': model.title,
                'special': model.special,
                'as_tab': model.as_tab,
                'criteria': model.criteria
                }
    
    def submit_form(self, request, form, target):
        target.name = form.cleaned_data['name']
        target.name_slug = slugify(form.cleaned_data['name'])
        target.description = form.cleaned_data['description']
        target.style = form.cleaned_data['style']
        target.title = form.cleaned_data['title']
        target.special = form.cleaned_data['special']
        target.as_tab = form.cleaned_data['as_tab']
        target.criteria = form.cleaned_data['criteria']
        target.save(force_update=True)
        return target, Message(_('Changes in rank "%(name)s" have been saved.') % {'name': self.original_name}, 'success')


class Delete(ButtonWidget):
    admin = site.get_action('ranks')
    id = 'delete'
    fallback = 'admin_users_ranks'
    notfound_message = _('Requested Rank could not be found.')
    
    def action(self, request, target):
        target.delete()
        return Message(_('Rank "%(name)s" has been deleted.') % {'name': target.name}, 'success'), False