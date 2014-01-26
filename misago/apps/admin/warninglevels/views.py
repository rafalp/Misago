from django.core.urlresolvers import reverse as django_reverse
from django.utils.translation import ugettext as _
import floppyforms as forms
from misago import messages
from misago.admin import site
from misago.apps.admin.widgets import *
from misago.forms import Form
from misago.models import WarnLevel
from misago.utils.strings import slugify
from misago.apps.admin.warninglevels.forms import WarnLevelForm

def reverse(route, target=None):
    if target:
        return django_reverse(route, kwargs={'target': target.pk, 'slug': slugify(target.name)})
    return django_reverse(route)


"""
Views
"""
class List(ListWidget):
    admin = site.get_action('warning_levels')
    id = 'list'
    columns = (
               ('name', _("Level Name")),
               )
    table_form_button = _('Change Warning Levels')
    nothing_checked_message = _('You have to check at least one warning level.')
    actions = (
               ('delete', _("Delete selected levels"), _("Are you sure you want to delete selected warning levels?")),
               )

    def get_table_form(self, page_items):
        order_form = {}

        # Build choices list
        choices = []
        for i in range(0, len(page_items)):
           choices.append([str(i), i + 1])

        # Build selectors list
        position = 0
        for item in page_items:
            order_form['pos_' + str(item.pk)] = forms.ChoiceField(choices=choices, initial=str(position))
            position += 1

        # Turn dict into object
        return type('OrderWarningLevelsForm', (Form,), order_form)

    def table_action(self, page_items, cleaned_data):
        for item in page_items:
            item.warning_level = cleaned_data['pos_' + str(item.pk)]
            item.save(force_update=True)
        WarnLevel.objects.flush_cache()
        return Message(_('Warning levels have been changed'), messages.SUCCESS), reverse('admin_warning_levels')

    def sort_items(self, page_items, sorting_method):
        return page_items.order_by('warning_level')

    def get_item_actions(self, item):
        return (
                self.action('pencil', _("Edit Level"), reverse('admin_warning_levels_edit', item)),
                self.action('remove', _("Delete Level"), reverse('admin_warning_levels_delete', item), post=True, prompt=_("Are you sure you want to delete this warning level?")),
                )

    def action_delete(self, items, checked):
        WarnLevel.objects.filter(id__in=checked).delete()

        levels_counter = 1
        for level in WarnLevel.objects.order_by('warning_level').iterator():
            if level.warning_level != levels_counter:
                level.warning_level = levels_counter
                level.save(force_update=True)
            levels_counter += 1
        WarnLevel.objects.flush_cache()

        return Message(_('Selected warning levels have been deleted successfully.'), messages.SUCCESS), reverse('admin_warning_levels')


class New(FormWidget):
    admin = site.get_action('warning_levels')
    id = 'new'
    fallback = 'admin_warning_levels'
    form = WarnLevelForm
    submit_button = _("Save Warning Level")

    def get_new_link(self, model):
        return reverse('admin_warning_levels_new')

    def get_edit_link(self, model):
        return reverse('admin_warning_levels_edit', model)

    def submit_form(self, form, target):
        top_level = WarnLevel.objects.order_by('-warning_level')[:1]
        if top_level:
            new_warning_level = top_level[0].warning_level + 1
        else:
            new_warning_level = 1

        new_level = WarnLevel(
                              name=form.cleaned_data['name'],
                              slug=slugify(form.cleaned_data['name']),
                              description=form.cleaned_data['description'],
                              warning_level=new_warning_level,
                              expires_after_minutes=form.cleaned_data['expires_after_minutes'],
                              restrict_posting_replies=form.cleaned_data['restrict_posting_replies'],
                              restrict_posting_threads=form.cleaned_data['restrict_posting_threads']
                              )
        new_level.save(force_insert=True)
        WarnLevel.objects.flush_cache()
        return new_level, Message(_('New warning level has been defined.'), messages.SUCCESS)


class Edit(FormWidget):
    admin = site.get_action('warning_levels')
    id = 'edit'
    name = _("Edit Warning Level")
    fallback = 'admin_warning_levels'
    form = WarnLevelForm
    target_name = 'name'
    notfound_message = _('Requested warning level could not be found.')
    translate_target_name = False
    submit_fallback = True

    def get_link(self, model):
        return reverse('admin_warning_levels_edit', model)

    def get_edit_link(self, model):
        return self.get_link(model)

    def get_initial_data(self, model):
        return {
                'name': model.name,
                'description': model.description,
                'expires_after_minutes': model.expires_after_minutes,
                'restrict_posting_replies': model.restrict_posting_replies,
                'restrict_posting_threads': model.restrict_posting_threads,
                }

    def submit_form(self, form, target):
        target.name = form.cleaned_data['name']
        target.slug = slugify(form.cleaned_data['name'])
        target.description = form.cleaned_data['description']
        target.expires_after_minutes = form.cleaned_data['expires_after_minutes']
        target.restrict_posting_replies = form.cleaned_data['restrict_posting_replies']
        target.restrict_posting_threads = form.cleaned_data['restrict_posting_threads']
        target.save(force_update=True)
        WarnLevel.objects.flush_cache()

        return target, Message(_('Changes in warning level "%(name)s" have been saved.') % {'name': self.original_name}, messages.SUCCESS)


class Delete(ButtonWidget):
    admin = site.get_action('warning_levels')
    id = 'delete'
    fallback = 'admin_warning_levels'
    notfound_message = _('Requested warning level could not be found.')

    def action(self, target):
        target.delete()

        levels_counter = 1
        for level in WarnLevel.objects.order_by('warning_level').iterator():
            if level.warning_level != levels_counter:
                level.warning_level = levels_counter
                level.save(force_update=True)
            levels_counter += 1
        WarnLevel.objects.flush_cache()

        return Message(_('Warning level "%(name)s" has been deleted.') % {'name': _(target.name)}, messages.SUCCESS), False
