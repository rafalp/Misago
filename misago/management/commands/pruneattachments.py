from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from misago.models import Attachment

class Command(BaseCommand):
    """
    Prune Attachments
    This command removes attachments that were uploaded but not attached to any posts.
    """
    help = 'Prune orphaned attachments'
    def handle(self, *args, **options):
        date_cutoff = timezone.now() - timedelta(days=1)
        deleted_count = 0
        for attachment in Attachment.objects.filter(date__lt=date_cutoff).filter(post__isnull=True).iterator():
            attachment.delete()
            deleted_count += 1

        if deleted_count == 1:
            self.stdout.write('One orphaned attachment has been deleted.\n')
        else:
            self.stdout.write('%s orphaned attachments have been deleted.\n' % deleted_count)