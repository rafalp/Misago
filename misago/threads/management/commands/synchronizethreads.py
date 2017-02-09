import time

from django.core.management.base import BaseCommand

from misago.core.management.progressbar import show_progress
from misago.core.pgutils import batch_update
from misago.threads.models import Thread


class Command(BaseCommand):
    help = "Synchronizes threads"

    def handle(self, *args, **options):
        threads_to_sync = Thread.objects.count()

        if not threads_to_sync:
            self.stdout.write("\n\nNo threads were found")
        else:
            self.sync_threads(threads_to_sync)

    def sync_threads(self, threads_to_sync):
        message = "Synchronizing %s threads...\n"
        self.stdout.write(message % threads_to_sync)

        message = "\n\nSynchronized %s threads"

        synchronized_count = 0
        show_progress(self, synchronized_count, threads_to_sync)
        start_time = time.time()
        for thread in batch_update(Thread.objects.all()):
            thread.synchronize()
            thread.save()

            synchronized_count += 1
            show_progress(self, synchronized_count, threads_to_sync, start_time)

        self.stdout.write(message % synchronized_count)
