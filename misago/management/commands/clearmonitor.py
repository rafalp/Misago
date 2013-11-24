from django.core.management.base import BaseCommand
from misago.models import MonitorItem

class Command(BaseCommand):
    help = 'Clears forum monitor'

    def handle(self, *args, **options):
        MonitorItem.objects.filter(_value__isnull=True).delete()
        self.stdout.write('\nForum monitor has been cleared.\n')
