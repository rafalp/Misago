from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from misago.setup.fixtures import load_app_fixtures
from misago.monitor.models import Item
from optparse import make_option

class Command(BaseCommand):
    """
    Loads Misago fixtures
    """
    help = 'Load Misago fixtures'
    def handle(self, *args, **options):
        if Item.objects.count() > 0:
            self.stdout.write("\nIt appears that fixters have been loaded already. Use updatefixtures if you want to update database data.\n")
        else:
            fixtures = 0
            for app in settings.INSTALLED_APPS:
                if load_app_fixtures(app):
                    fixtures += 1
                    print 'Loading fixtures from %s' % app
            self.stdout.write('\nLoaded fixtures from %s applications.\n' % fixtures)
