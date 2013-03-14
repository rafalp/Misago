from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import (connections, router, transaction, DEFAULT_DB_ALIAS,
      IntegrityError, DatabaseError)
from django.utils import timezone
from misago.setup.fixtures import load_app_fixtures, update_app_fixtures
from misago.setup.models import Fixture
from optparse import make_option

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
            fixture_data[fixture.app_name] = fixture
        loaded = 0
        updated = 0
        
        for app in settings.INSTALLED_APPS_COMPLETE:
            if app in fixture_data:
                if update_app_fixtures(app):
                    updated += 1
                    if not options['quiet']:
                        self.stdout.write('Updating fixtures from %s' % app)
            else:
                if load_app_fixtures(app):
                    loaded += 1
                    Fixture.objects.create(app_name=app)
                    if not options['quiet']:
                        self.stdout.write('Loading fixtures from %s' % app)
        
        if not options['quiet']:
            self.stdout.write('\nLoaded %s fixtures and updated %s fixtures.\n' % (loaded, updated))