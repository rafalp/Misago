from django.core.management.base import BaseCommand
from misago.models import User

class Command(BaseCommand):
    help = 'Updates unread Private Threads counters update for all users'

    def handle(self, *args, **options):
        User.objects.update(sync_pds=True)
        self.stdout.write('\nUsers accounts were set to sync unread private threads stat on next visit.\n')
