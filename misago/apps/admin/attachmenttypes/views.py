from django.core.urlresolvers import reverse as django_reverse
from django.utils.translation import ugettext as _
import floppyforms as forms
from misago import messages
from misago.admin import site
from misago.apps.admin.widgets import *
from misago.forms import Form
from misago.models import AttachmentType
from misago.utils.strings import slugify
from misago.apps.admin.attachmenttypes.forms import AttachmentTypeForm

def reverse(route, target=None):
    if target:
        return django_reverse(route, kwargs={'target': target.pk, 'slug': slugify(target.name)})
    return django_reverse(route)


"""
Views
"""
class List(ListWidget):
    admin = site.get_action('attachments')
    id = 'list'
    columns = (
               ('name', _("Type Name")),
               ('extensions', _("File Extensions")),
               )

    def sort_items(self, page_items, sorting_method):
        return page_items.order_by('name')

    def get_item_actions(self, item):
        return (
                self.action('pencil', _("Edit Type"), reverse('admin_attachments_types_edit', item)),
                self.action('remove', _("Delete Type"), reverse('admin_attachments_types_delete', item)),
                )

class New(FormWidget):
    admin = site.get_action('attachments')
    id = 'new'
    fallback = 'admin_attachments_types'
    form = AttachmentTypeForm
    submit_button = _("Save Type")

    def get_new_link(self, model):
        return reverse('admin_attachments_types_new')

    def get_edit_link(self, model):
        return reverse('admin_attachments_types_edit', model)

    def submit_form(self, form, target):
        new_type = AttachmentType(
                                  name=form.cleaned_data['name'],
                                  extensions=form.cleaned_data['extensions'],
                                  size_limit=form.cleaned_data['size_limit'],
                                  )
        new_type.save(force_insert=True)
        for role in form.cleaned_data['roles']:
            new_type.roles.add(roles)
        AttachmentType.objects.flush_cache()
        return new_type, Message(_('New attachments type has been created.'), messages.SUCCESS)


class Edit(FormWidget):
    admin = site.get_action('attachments')
    id = 'edit'
    name = _("Edit Attachment Type")
    fallback = 'admin_attachments_types'
    form = AttachmentTypeForm
    target_name = 'name'
    notfound_message = _('Requested attachments type could not be found.')
    translate_target_name = True
    submit_fallback = True

    def get_link(self, model):
        return reverse('admin_attachments_types_edit', model)

    def get_edit_link(self, model):
        return self.get_link(model)

    def get_initial_data(self, model):
        return {
                'name': model.name,
                'extensions': model.extensions,
                'size_limit': model.size_limit,
                'roles': model.roles,
                }

    def submit_form(self, form, target):
        target.name = form.cleaned_data['name']
        target.extensions = form.cleaned_data['extensions']
        target.size_limit = form.cleaned_data['size_limit']
        target.save(force_update=True)

        target.update_roles(form.cleaned_data['roles'])
        AttachmentType.objects.flush_cache()

        return target, Message(_('Changes in type "%(name)s" have been saved.') % {'name': self.original_name}, messages.SUCCESS)


class Delete(FormWidget):
    admin = site.get_action('attachments')
    id = 'delete'
    name = _("Delete Attachment Type")
    fallback = 'admin_attachments_types'
    form = AttachmentTypeForm
    target_name = 'name'
    notfound_message = _('Requested attachments type could not be found.')
    submit_fallback = True
    template = 'delete'

    def get_link(self, model):
        return reverse('admin_attachments_types_delete', model)

    def __call__(self, request, target=None, slug=None):
        self.request = request

        # Fetch target
        model = None
        if target:
            model = self.get_and_validate_target(target)
            self.original_name = self.get_target_name(model)
            if not model:
                return redirect(self.get_fallback_link())
        original_model = model

        message = None
        if request.method == 'POST':
            if request.csrf.request_secure(request):
                if model.attachment_set.count():
                    deleted = 0
                    for attachment in model.attachment_set.iterator():
                        attachment.delete()
                        deleted += 1
                    messages.success(request, ungettext(
                                                        'Attachment type and one attachment has been deleted.',
                                                        'Attachment type and %(deleted)d attachments have been deleted.',
                                                        deleted
                                                        ) % {'deleted': deleted}, self.admin.id)
                else:
                    messages.info(request, _("Attachment type has been deleted."), self.admin.id)
                model.delete()
                AttachmentType.objects.flush_cache()
                return redirect(reverse('admin_attachments_types'))
            else:
                message = Message(_("Request authorization is invalid. Please resubmit your form."), messages.ERROR)

        return render_to_response(self.get_template(),
                                  {
                                  'admin': self.admin,
                                  'action': self,
                                  'request': request,
                                  'link': self.get_link(model),
                                  'fallback': self.get_fallback_link(),
                                  'messages': messages.get_messages(request, self.admin.id),
                                  'message': message,
                                  'tabbed': self.tabbed,
                                  'attachments_count': model.attachment_set.count(),
                                  'target': self.get_target_name(original_model),
                                  'target_model': original_model,
                                  },
                                  context_instance=RequestContext(request));
