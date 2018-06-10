import time

from django.core.management.base import BaseCommand

from misago.core.management.progressbar import show_progress
from misago.core.pgutils import chunk_queryset
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
        self.stdout.write("Synchronizing {} threads...\n".format(threads_to_sync))

        synchronized_count = 0
        show_progress(self, synchronized_count, threads_to_sync)
        start_time = time.time()

        for thread in chunk_queryset(Thread.objects.all()):
            thread.synchronize()
            thread.save()

            synchronized_count += 1
            show_progress(self, synchronized_count, threads_to_sync, start_time)

        self.stdout.write("\n\nSynchronized {} threads".format(synchronized_count))
