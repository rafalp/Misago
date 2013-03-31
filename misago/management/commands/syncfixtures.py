from optparse import make_option
import traceback
import os.path
import pkgutil
from django.core.management.base import BaseCommand
from misago.models import Fixture
from misago.utils.fixtures import load_fixture, update_fixture
import misago.fixtures

class Command(BaseCommand):
    """
    Loads Misago fixtures
    """
    help = 'Load Misago fixtures'
    option_list = BaseCommand.option_list + (
        make_option('--quiet',
            action='store_true',
            dest='quiet',
            default=False,
            help='Dont display output from this message'),
        )
    
    def handle(self, *args, **options):
        if not options['quiet']:
            self.stdout.write('\nLoading data from fixtures...')
            
        fixture_data = {}
        for fixture in Fixture.objects.all():
            fixture_data[fixture.name] = fixture

        loaded = 0
        updated = 0
        
        fixtures_path = os.path.dirname(misago.fixtures.__file__)
        try:
            for _, name, _ in pkgutil.iter_modules([fixtures_path]):
                if name in fixture_data:
                    if update_fixture('misago.fixtures.' + name):
                        updated += 1
                        if not options['quiet']:
                            self.stdout.write('Updating "%s" fixture...' % name)
                else:
                    if load_fixture('misago.fixtures.' + name):
                        loaded += 1
                        Fixture.objects.create(name=name)
                        if not options['quiet']:
                            self.stdout.write('Loading "%s" fixture...' % name)
        except:
            self.stderr.write(traceback.format_exc())

        if not options['quiet']:
            self.stdout.write('\nLoaded %s fixtures and updated %s fixtures.\n' % (loaded, updated))
