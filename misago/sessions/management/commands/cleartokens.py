from datetime import timedelta
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from optparse import make_option
from misago.sessions.models import Token

class Command(BaseCommand):
    """
    This command is intended to work as CRON job fired every few days to remove unused tokens 
    """
    help = 'Clears "Remember Me" tokens'
    def handle(self, *args, **options):
        Token.objects.filter(accessed__lte=timezone.now() - timedelta(days=5)).delete()
        self.stdout.write('Sessions tokens have been cleared.\n')        