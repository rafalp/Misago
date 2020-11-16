import time
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from ....conf.shortcuts import get_dynamic_settings
from ....core.management.progressbar import show_progress
from ....core.pgutils import chunk_queryset
from ...models import Attachment


class Command(BaseCommand):
    help = "Deletes attachments unassociated with any posts"

    def handle(self, *args, **options):
        settings = get_dynamic_settings()

        cutoff = timezone.now() - timedelta(hours=settings.unused_attachments_lifetime)
        queryset = Attachment.objects.filter(post__isnull=True, uploaded_on__lt=cutoff)

        attachments_to_sync = queryset.count()

        if not attachments_to_sync:
            self.stdout.write("\n\nNo unused attachments were cleared")
        else:
            self.sync_attachments(queryset, attachments_to_sync)

    def sync_attachments(self, queryset, attachments_to_sync):
        self.stdout.write("Clearing %s attachments...\n" % attachments_to_sync)

        cleared_count = 0
        show_progress(self, cleared_count, attachments_to_sync)
        start_time = time.time()

        for attachment in chunk_queryset(queryset):
            attachment.delete()

            cleared_count += 1
            show_progress(self, cleared_count, attachments_to_sync, start_time)

        self.stdout.write("\n\nCleared %s attachments" % cleared_count)
