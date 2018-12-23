import time

from django.core.management.base import BaseCommand

from ....core.management.progressbar import show_progress
from ...models import Category


class Command(BaseCommand):
    help = "Synchronizes categories"

    def handle(self, *args, **options):
        categories_to_sync = Category.objects.count()

        message = "Synchronizing %s categories...\n"
        self.stdout.write(message % categories_to_sync)

        message = "\n\nSynchronized %s categories in %s"

        start_time = time.time()

        synchronized_count = 0
        show_progress(self, synchronized_count, categories_to_sync)
        for category in Category.objects.iterator():
            category.synchronize()
            category.save()

            synchronized_count += 1
            show_progress(self, synchronized_count, categories_to_sync)

        end_time = time.time() - start_time
        total_time = time.strftime("%H:%M:%S", time.gmtime(end_time))

        self.stdout.write(message % (synchronized_count, total_time))
