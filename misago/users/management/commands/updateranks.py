from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from optparse import make_option

class Command(BaseCommand):
    """
    This command is intended to work as CRON job fired of once per day or less if you have more users.
    """
    help = 'Updates users ranking'
    def handle(self):
        self.stdout.write('Users ranking has been updated.\n')