from datetime import timedelta
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from misago.sessions.models import Session

class Command(BaseCommand):
    """
    This command is intended to work as CRON job fired every few hours to keep sessions table reasonable 
    """
    help = 'Clears users sessions'
    def handle(self, *args, **options):
        Session.objects.filter(last__lte=timezone.now() - timedelta(seconds=settings.SESSION_LIFETIME)).delete()
        self.stdout.write('Sessions have been cleared.\n')