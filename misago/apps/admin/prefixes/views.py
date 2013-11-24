from django.core.urlresolvers import reverse as django_reverse
from django.utils.translation import ugettext as _
import floppyforms as forms
from misago import messages
from misago.admin import site
from misago.apps.admin.widgets import *
from misago.forms import Form
from misago.models import ThreadPrefix
from misago.utils.strings import slugify
from misago.apps.admin.prefixes.forms import PrefixForm

def reverse(route, target=None):
    if target:
        return django_reverse(route, kwargs={'target': target.pk, 'slug': slugify(target.name)})
    return django_reverse(route)


"""
Views
"""
class List(ListWidget):
    admin = site.get_action('prefixes')
    id = 'list'
    columns = (
               ('prefix', _("Thread Prefix")),
               )
    nothing_checked_message = _('You have to check at least one prefix.')
    actions = (
               ('delete', _("Delete selected prefixes"), _("Are you sure you want to delete selected prefixes?")),
               )

    def sort_items(self, page_items, sorting_method):
        return page_items.order_by('name')

    def get_item_actions(self, item):
        return (
                self.action('pencil', _("Edit Prefix"), reverse('admin_threads_prefixes_edit', item)),
                self.action('remove', _("Delete Prefix"), reverse('admin_threads_prefixes_delete', item), post=True, prompt=_("Are you sure you want to delete this prefix?")),
                )

    def action_delete(self, items, checked):
        for prefix in ThreadPrefix.objects.filter(id__in=checked):
            prefix.delete()
        return Message(_('Selected prefixes have been deleted successfully.'), messages.SUCCESS), reverse('admin_threads_prefixes')


class New(FormWidget):
    admin = site.get_action('prefixes')
    id = 'new'
    fallback = 'admin_threads_prefixes'
    form = PrefixForm
    submit_button = _("Save Prefix")

    def get_new_link(self, model):
        return reverse('admin_threads_prefixes_new')

    def get_edit_link(self, model):
        return reverse('admin_threads_prefixes_edit', model)

    def submit_form(self, form, target):
        new_prefix = ThreadPrefix(
                                  name=form.cleaned_data['name'],
                                  slug=slugify(form.cleaned_data['name']),
                                  style=form.cleaned_data['style'],
                                  )
        new_prefix.save(force_insert=True)
        for forum in form.cleaned_data['forums']:
            new_prefix.forums.add(forum)
        return new_prefix, Message(_('New Prefix has been created.'), messages.SUCCESS)


class Edit(FormWidget):
    admin = site.get_action('prefixes')
    id = 'edit'
    name = _("Edit Prefix")
    fallback = 'admin_threads_prefixes'
    form = PrefixForm
    target_name = 'name'
    notfound_message = _('Requested Prefix could not be found.')
    translate_target_name = True
    submit_fallback = True

    def get_link(self, model):
        return reverse('admin_threads_prefixes_edit', model)

    def get_edit_link(self, model):
        return self.get_link(model)

    def get_initial_data(self, model):
        return {
                'name': model.name,
                'style': model.style,
                'forums': model.forums.all(),
                }

    def submit_form(self, form, target):
        target.name = form.cleaned_data['name']
        target.slug = slugify(form.cleaned_data['name'])
        target.style = form.cleaned_data['style']
        target.save(force_update=True)

        target.update_forums(form.cleaned_data['forums'])

        return target, Message(_('Changes in prefix "%(name)s" have been saved.') % {'name': self.original_name}, messages.SUCCESS)


class Delete(ButtonWidget):
    admin = site.get_action('prefixes')
    id = 'delete'
    fallback = 'admin_threads_prefixes'
    notfound_message = _('Requested Prefix could not be found.')

    def action(self, target):
        target.delete()
        return Message(_('Prefix "%(name)s" has been deleted.') % {'name': _(target.name)}, messages.SUCCESS), False
