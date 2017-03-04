from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from misago.conf import settings
from misago.readtracker.models import CategoryRead, ThreadRead


class Command(BaseCommand):
    help = "Deletes expired records from readtracker"

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(days=settings.MISAGO_READTRACKER_CUTOFF)

        categories = CategoryRead.objects.filter(last_read_on__lte=cutoff)
        threads = ThreadRead.objects.filter(last_read_on__lte=cutoff)

        total_count = categories.count() + threads.count()

        if total_count:
            categories.delete()
            threads.delete()

            message = "\n\nDeleted %s expired entries" % total_count
        else:
            message = "\n\nNo expired entries were found"

        self.stdout.write(message)
