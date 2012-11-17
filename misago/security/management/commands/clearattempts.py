from datetime import timedelta
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from misago.security.models import SignInAttempt

class Command(BaseCommand):
    """
    This command is intended to work as CRON job fired every few days to remove failed sign-in attempts
    """
    help = 'Clears sign-in attempts log'
    def handle(self):
        SignInAttempt.objects.filter(date__lte=timezone.now() - timedelta(hours=24)).delete()
        self.stdout.write('Failed Sign-In attempts older than 24h have been removed.\n')