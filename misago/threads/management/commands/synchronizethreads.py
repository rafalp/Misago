import time

from django.core.management.base import BaseCommand, CommandError

from ....core.management.progressbar import show_progress
from ...models import Thread
from ...synchronize import synchronize_thread


class Command(BaseCommand):
    help = "Synchronizes threads"

    def handle(self, *args, **options):
        threads_to_sync = Thread.objects.count()

        if not threads_to_sync:
            raise CommandError("No threads exist.")

        if threads_to_sync == 1:
            self.stdout.write("Synchronizing one thread...\n")
        else:
            self.stdout.write(f"Synchronizing {threads_to_sync} threads...\n")

        synchronized_count = 0
        show_progress(self, synchronized_count, threads_to_sync)
        start_time = time.time()

        for thread in Thread.objects.iterator(chunk_size=50):
            synchronize_thread(thread)

            synchronized_count += 1
            show_progress(self, synchronized_count, threads_to_sync, start_time)

        if threads_to_sync == 1:
            self.stdout.write(f"\nSynchronized one thread.")
        else:
            self.stdout.write(f"\nSynchronized {threads_to_sync} threads.")
