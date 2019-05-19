from django.contrib import messages
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from ....admin.views import generic
from ...models import AttachmentType
from ..forms import AttachmentTypeForm


class AttachmentTypeAdmin(generic.AdminBaseMixin):
    root_link = "misago:admin:settings:attachment-types:index"
    model = AttachmentType
    form_class = AttachmentTypeForm
    templates_dir = "misago/admin/attachmenttypes"
    message_404 = _("Requested attachment type could not be found.")

    def update_roles(self, target, roles):
        target.roles.clear()
        if roles:
            target.roles.add(*roles)

    def handle_form(self, form, request, target):
        super().handle_form(form, request, target)
        form.save()


class AttachmentTypesList(AttachmentTypeAdmin, generic.ListView):
    ordering = (("name", None),)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.annotate(num_files=Count("attachment"))


class NewAttachmentType(AttachmentTypeAdmin, generic.ModelFormView):
    message_submit = _('New type "%(name)s" has been saved.')


class EditAttachmentType(AttachmentTypeAdmin, generic.ModelFormView):
    message_submit = _('Attachment type "%(name)s" has been edited.')


class DeleteAttachmentType(AttachmentTypeAdmin, generic.ButtonView):
    def check_permissions(self, request, target):
        if target.attachment_set.exists():
            message = _(
                'Attachment type "%(name)s" has '
                "associated attachments and can't be deleted."
            )
            return message % {"name": target.name}

    def button_action(self, request, target):
        target.delete()
        message = _('Attachment type "%(name)s" has been deleted.')
        messages.success(request, message % {"name": target.name})
