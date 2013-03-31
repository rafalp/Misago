from optparse import make_option
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    """
    Builds Misago database from scratch
    """
    help = 'Install Misago to database'
    option_list = BaseCommand.option_list + (
        make_option('--quiet',
            action='store_true',
            dest='quiet',
            default=False,
            help='Dont display output from this message'),
        )
    
    def handle(self, *args, **options):
        if not options['quiet']:
            self.stdout.write('\nInstalling Misago to database...')

        if options['quiet']:
            call_command('syncdb', verbosity=0)
            call_command('migrate', verbosity=0)
            call_command('syncfixtures', quiet=1)
        else:
            call_command('syncdb')
            call_command('migrate')
            call_command('syncfixtures')

        if not options['quiet']:
            self.stdout.write('\nInstallation complete! Don\'t forget to run adduser to create first admin!\n')