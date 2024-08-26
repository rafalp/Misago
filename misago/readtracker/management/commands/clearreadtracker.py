from django.core.management.base import BaseCommand

from ....conf.shortcuts import get_dynamic_settings
from ...readtime import get_default_read_time
from ...models import ReadCategory, ReadThread


class Command(BaseCommand):
    help = "Deletes expired read times from the database"

    def handle(self, *args, **options):
        settings = get_dynamic_settings()
        default_read_time = get_default_read_time(settings)

        deleted_categories, _ = ReadCategory.objects.filter(
            read_time__lte=default_read_time
        ).delete()

        deleted_threads, _ = ReadThread.objects.filter(
            read_time__lte=default_read_time
        ).delete()

        self.stdout.write("Expired read times deleted:")
        self.stdout.write(f" - Categories:   {deleted_categories}")
        self.stdout.write(f" - Threads:      {deleted_threads}")

        self.stdout.write("\nRemaining:")
        self.stdout.write(f" - Categories:   {ReadCategory.objects.count()}")
        self.stdout.write(f" - Threads:      {ReadThread.objects.count()}")
