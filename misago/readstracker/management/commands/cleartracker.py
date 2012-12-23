from datetime import timedelta
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from misago.readstracker.models import Record

class Command(BaseCommand):
    """
    This command is intended to work as CRON job fired every few days to remove old reads tracker entries
    """
    help = 'Clears Reads Tracker memory'
    def handle(self, *args, **options):
        Record.objects.filter(updated__lte=timezone.now() - timedelta(days=settings.READS_TRACKER_LENGTH)).delete()
        self.stdout.write('Reads tracker has been cleared.\n')        