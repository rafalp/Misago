from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    """
    Updates Misago to latest version
    """
    help = 'Update Misago database to latest version'
    
    def handle(self, *args, **options):
        self.stdout.write('\nUpdating Misago database to latest version...')
        call_command('migrate')
        call_command('initdata')
        self.stdout.write('\nUpdate complete!\n')