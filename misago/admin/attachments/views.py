from django.contrib import messages
from django.db import transaction
from django.utils.translation import pgettext, pgettext_lazy

from ...attachments.filetypes import filetypes
from ...attachments.models import Attachment
from ...threads.models import Post
from ..views import generic
from .forms import FilterAttachmentsForm


class AttachmentAdmin(generic.AdminBaseMixin):
    root_link = "misago:admin:attachments:index"
    model = Attachment
    templates_dir = "misago/admin/attachments"
    message_404 = pgettext_lazy(
        "admin attachments", "Requested attachment does not exist."
    )

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related("uploader", "post", "post__thread", "post__category")


class AttachmentsList(AttachmentAdmin, generic.ListView):
    items_per_page = 20
    ordering = [
        ("-id", pgettext_lazy("admin attachments ordering choice", "From newest")),
        ("id", pgettext_lazy("admin attachments ordering choice", "From oldest")),
        ("filename", pgettext_lazy("admin attachments ordering choice", "A to z")),
        ("-filename", pgettext_lazy("admin attachments ordering choice", "Z to a")),
        ("size", pgettext_lazy("admin attachments ordering choice", "Smallest files")),
        ("-size", pgettext_lazy("admin attachments ordering choice", "Largest files")),
    ]
    selection_label = pgettext_lazy("admin attachments", "With attachments: 0")
    empty_selection_label = pgettext_lazy("admin attachments", "Select attachments")
    mass_actions = [
        {
            "action": "delete",
            "name": pgettext_lazy("admin attachments", "Delete attachments"),
            "confirmation": pgettext_lazy(
                "admin attachments",
                "Are you sure you want to delete selected attachments?",
            ),
            "is_atomic": False,
        }
    ]
    filter_form = FilterAttachmentsForm

    def action_delete(self, request, attachments):
        deleted_attachments = []
        desynced_posts = []

        for attachment in attachments:
            if attachment.post:
                deleted_attachments.append(attachment.pk)
                desynced_posts.append(attachment.post_id)

        if desynced_posts:
            with transaction.atomic():
                for post in Post.objects.filter(id__in=desynced_posts):
                    self.delete_from_cache(post, deleted_attachments)

        for attachment in attachments:
            attachment.delete()

        message = pgettext(
            "admin attachments", "Selected attachments have been deleted."
        )
        messages.success(request, message)

    def delete_from_cache(self, post, attachments):
        if not post.attachments_cache:
            return  # admin action may be taken due to desynced state

        clean_cache = []
        for a in post.attachments_cache:
            if a["id"] not in attachments:
                clean_cache.append(a)

        post.attachments_cache = clean_cache or None
        post.save(update_fields=["attachments_cache"])


class DeleteAttachment(AttachmentAdmin, generic.ButtonView):
    def button_action(self, request, target):
        if target.post:
            self.delete_from_cache(target)
        target.delete()
        message = pgettext(
            "admin attachments", 'Attachment "%(name)s" has been deleted.'
        )
        messages.success(request, message % {"name": target.name})

    def delete_from_cache(self, attachment):
        if not attachment.post.attachments_cache:
            return  # admin action may be taken due to desynced state

        clean_cache = []
        for a in attachment.post.attachments_cache:
            if a["id"] != attachment.id:
                clean_cache.append(a)

        attachment.post.attachments_cache = clean_cache or None
        attachment.post.save(update_fields=["attachments_cache"])


class AttachmentsFiletypesList(generic.AdminView):
    root_link = "misago:admin:attachments:filetypes:index"
    templates_dir = "misago/admin/attachments_filetypes"
    template_name = "list.html"

    def get(self, request):
        return self.render(request, {"items": filetypes.get_all_filetypes()})
