from django.core.management.base import BaseCommand
from misago.models import Session

class Command(BaseCommand):
    """
    Maintenance command for emptying sessions tab
    """
    help = 'Clears users sessions'
    def handle(self, *args, **options):
        Session.objects.all().delete()
        self.stdout.write('\nSessions have been emptied.\n')