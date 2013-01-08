from django.core.management.base import BaseCommand
from django.utils import timezone
from optparse import make_option
from misago.monitor.monitor import Monitor
from misago.users.models import User

class Command(BaseCommand):
    help = 'Updates forum monitor to contain to date user information'

    def handle(self, *args, **options):
        User.objects.resync_monitor(Monitor())
        self.stdout.write('\n\nForum monitor has been updated to contain to date user information.\n')
