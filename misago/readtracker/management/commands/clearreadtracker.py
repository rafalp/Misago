from django.core.management.base import BaseCommand

from misago.readtracker.dates import get_cutoff_date
from misago.readtracker.models import PostRead


class Command(BaseCommand):
    help = "Deletes expired records from readtracker"

    def handle(self, *args, **options):
        queryset = PostRead.objects.filter(last_read_on__lt=get_cutoff_date())
        deleted_count = queryset.count()

        if deleted_count:
            queryset.delete()

            message = "\n\nDeleted %s expired entries" % deleted_count
        else:
            message = "\n\nNo expired entries were found"

        self.stdout.write(message)
