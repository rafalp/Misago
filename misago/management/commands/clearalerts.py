from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from misago.models import Alert

class Command(BaseCommand):
    """
    This command is intended to work as CRON job fired every few days to delete old alerts
    """
    help = 'Clears old alerts'
    def handle(self, *args, **options):
        Alert.objects.filter(date__lte=timezone.now() - timedelta(days=14)).delete()
        self.stdout.write('Old Alerts have been cleared.\n')
