from django.core.management.base import BaseCommand

from misago.categories.models import Category
from misago.core.management.progressbar import show_progress


class Command(BaseCommand):
    help = 'Synchronizes categories'

    def handle(self, *args, **options):
        categories_to_sync = Category.objects.count()

        message = 'Synchronizing %s categories...\n'
        self.stdout.write(message % categories_to_sync)

        message = '\n\nSynchronized %s categories'

        synchronized_count = 0
        show_progress(self, synchronized_count, categories_to_sync)
        for category in Category.objects.iterator():
            category.synchronize()
            category.save()

            synchronized_count += 1
            show_progress(self, synchronized_count, categories_to_sync)

        self.stdout.write(message % synchronized_count)
