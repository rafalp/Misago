from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from misago.setup.fixtures import update_app_fixtures
from optparse import make_option

class Command(BaseCommand):
    """
    Updates Misago fixtures
    """
    help = 'Update Misago fixtures'
    def handle(self, *args, **options):
        fixtures = 0
        for app in settings.INSTALLED_APPS:
            if update_app_fixtures(app):
                fixtures += 1
                print 'Updating fixtures from %s' % app
        self.stdout.write('\nUpdated fixtures from %s applications.\n' % fixtures)
