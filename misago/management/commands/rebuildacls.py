from django.core.management.base import BaseCommand
from misago.monitor import monitor, UpdatingMonitor

class Command(BaseCommand):
    help = 'Rebuilds ACLs for all users'

    def handle(self, *args, **options):
        with UpdatingMonitor() as cm:
            monitor.increase('acl_version')
        self.stdout.write('\nUser ACLs cache has been set as outdated and will be rebuild when needed.\n')
