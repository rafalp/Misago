from django.core.management.base import BaseCommand
from misago.monitor import Monitor

class Command(BaseCommand):
    help = 'Rebuilds ACLs for all users'

    def handle(self, *args, **options):
        monitor = Monitor()
        monitor['acl_version'] = int(monitor['acl_version']) + 1
        self.stdout.write('\nUser ACLs cache has been set as outdated and will be rebuild when needed.\n')
