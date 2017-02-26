from django.contrib import messages
from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from misago.admin.views import generic
from misago.threads.forms import SearchAttachmentsForm
from misago.threads.models import Attachment, Post


class AttachmentAdmin(generic.AdminBaseMixin):
    root_link = 'misago:admin:system:attachments:index'
    model = Attachment
    templates_dir = 'misago/admin/attachments'
    message_404 = _("Requested attachment could not be found.")

    def get_queryset(self):
        qs = super(AttachmentAdmin, self).get_queryset()
        return qs.select_related('filetype', 'uploader', 'post', 'post__thread', 'post__category')


class AttachmentsList(AttachmentAdmin, generic.ListView):
    items_per_page = 20
    ordering = [
        ('-id', _("From newest")),
        ('id', _("From oldest")),
        ('filename', _("A to z")),
        ('-filename', _("Z to a")),
        ('size', _("Smallest files")),
        ('-size', _("Largest files")),
    ]
    selection_label = _('With attachments: 0')
    empty_selection_label = _('Select attachments')
    mass_actions = [
        {
            'action': 'delete',
            'name': _("Delete attachments"),
            'icon': 'fa fa-times-circle',
            'confirmation': _("Are you sure you want to delete selected attachments?"),
            'is_atomic': False,
        },
    ]

    def get_search_form(self, request):
        return SearchAttachmentsForm

    def action_delete(self, request, attachments):
        deleted_attachments = []
        desynced_posts = []

        for attachment in attachments:
            if attachment.post:
                deleted_attachments.append(attachment.pk)
                desynced_posts.append(attachment.post_id)

        if desynced_posts:
            with transaction.atomic():
                for post in Post.objects.select_for_update().filter(id__in=desynced_posts):
                    self.delete_from_cache(post, deleted_attachments)

        for attachment in attachments:
            attachment.delete()

        message = _("Selected attachments have been deleted.")
        messages.success(request, message)

    def delete_from_cache(self, post, attachments):
        if not post.attachments_cache:
            return  # admin action may be taken due to desynced state

        clean_cache = []
        for a in post.attachments_cache:
            if a['id'] not in attachments:
                clean_cache.append(a)

        post.attachments_cache = clean_cache or None
        post.save(update_fields=['attachments_cache'])


class DeleteAttachment(AttachmentAdmin, generic.ButtonView):
    def button_action(self, request, target):
        if target.post:
            self.delete_from_cache(target)
        target.delete()
        message = _('Attachment "%(filename)s" has been deleted.')
        messages.success(request, message % {'filename': target.filename})

    def delete_from_cache(self, attachment):
        if not attachment.post.attachments_cache:
            return  # admin action may be taken due to desynced state

        clean_cache = []
        for a in attachment.post.attachments_cache:
            if a['id'] != attachment.id:
                clean_cache.append(a)

        attachment.post.attachments_cache = clean_cache or None
        attachment.post.save(update_fields=['attachments_cache'])
