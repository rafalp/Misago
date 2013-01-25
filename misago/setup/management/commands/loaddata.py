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
    
    def handle(self, *args, **options):
        fixture_data = {}
        for fixture in Fixture.objects.all():
            fixture_data[fixture.app_name] = fixture
        loaded = 0
        updated = 0
        for app in settings.INSTALLED_APPS:
            if app in fixture_data:
                if update_app_fixtures(app):
                    updated += 1
                    print 'Updating fixtures from %s' % app
            else:
                if load_app_fixtures(app):
                    loaded += 1
                    print 'Loading fixtures from %s' % app
                    Fixture.objects.create(app_name=app)
        self.stdout.write('Loaded %s fixtures and updated %s fixtures.\n' % (loaded, updated))