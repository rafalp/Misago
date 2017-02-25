import time
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from misago.conf import settings
from misago.core.management.progressbar import show_progress
from misago.core.pgutils import batch_update
from misago.threads.models import Attachment


class Command(BaseCommand):
    help = "Deletes attachments unassociated with any posts"

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(minutes=settings.MISAGO_ATTACHMENT_ORPHANED_EXPIRE)
        queryset = Attachment.objects.filter(
            post__isnull=True,
            uploaded_on__lt=cutoff,
        )

        attachments_to_sync = queryset.count()

        if not attachments_to_sync:
            self.stdout.write("\n\nNo attachments were found")
        else:
            self.sync_attachments(queryset, attachments_to_sync)

    def sync_attachments(self, queryset, attachments_to_sync):
        message = "Clearing %s attachments...\n"
        self.stdout.write(message % attachments_to_sync)

        message = "\n\nCleared %s attachments"

        synchronized_count = 0
        show_progress(self, synchronized_count, attachments_to_sync)
        start_time = time.time()
        for attachment in batch_update(queryset):
            attachment.delete()

            synchronized_count += 1
            show_progress(self, synchronized_count, attachments_to_sync, start_time)

        self.stdout.write(message % synchronized_count)
