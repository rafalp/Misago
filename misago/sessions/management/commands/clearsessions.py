from datetime import timedelta
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from optparse import make_option
from misago.sessions.models import Session

class Command(BaseCommand):
    """
    This command is intended to work as CRON job fired every few hours to keep sessions table reasonable 
    """
    help = 'Clears users sessions'
    def handle(self, *args, **options):
        Session.objects.filter(last__lte=timezone.now() - timedelta(hours=12)).delete()
        self.stdout.write('Sessions have been cleared.\n')