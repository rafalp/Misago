from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    """
    Builds Misago database from scratch
    """
    help = 'Install Misago to database'
    
    def handle(self, *args, **options):
        self.stdout.write('\nInstalling Misago to database...')
        call_command('syncdb')
        call_command('migrate')
        call_command('initdata')
        self.stdout.write('\nInstallation complete! Don\'t forget to run adduser to create first admin!\n')