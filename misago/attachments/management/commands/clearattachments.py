import time
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from ....conf.shortcuts import get_dynamic_settings
from ...models import Attachment


class Command(BaseCommand):
    help = (
        "Deletes attachments that are marked for deletion or "
        "are not associated with any posts."
    )

    def handle(self, *args, **options):
        self.stdout.write("Attachments deleted:\n\n")
        self.delete_marked()
        self.delete_unused()

    def delete_marked(self):
        queryset = Attachment.objects.filter(is_deleted=True).order_by("id")

        deleted = queryset.count()
        for attachment in queryset.iterator(50):
            attachment.delete()

        self.stdout.write(f"- Marked: {deleted}")

    def delete_unused(self):
        settings = get_dynamic_settings()

        cutoff = timezone.now() - timedelta(hours=settings.unused_attachments_lifetime)
        queryset = Attachment.objects.filter(
            post__isnull=True, uploaded_at__lt=cutoff
        ).order_by("id")

        deleted = queryset.count()
        for attachment in queryset.iterator(50):
            attachment.delete()

        self.stdout.write(f"- Unused: {deleted}")
