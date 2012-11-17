from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from misago.setup.fixtures import load_app_fixtures
from optparse import make_option

class Command(BaseCommand):
    """
    Loads misago fixtures
    """
    help = 'Load Misago fixtures'
    def handle(self, *args, **options):
        fixtures = 0
        for app in settings.INSTALLED_APPS:
            if load_app_fixtures(app):
                fixtures += 1
                print 'Loading fixtures from %s' % app
        self.stdout.write('\nLoaded fixtures from %s applications.\n' % fixtures)