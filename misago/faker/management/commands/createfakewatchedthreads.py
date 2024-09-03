import random
import time

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from ....core.management.progressbar import show_progress
from ....notifications.models import WatchedThread
from ....threads.models import Thread

User = get_user_model()


class Command(BaseCommand):
    help = "Adds watched threads entries for all users and threads"

    def handle(self, *args, **options):
        total_users = User.objects.count()
        total_threads = Thread.objects.count()

        self.stdout.write(
            f"Creating watched thread entries for {total_users} users "
            f"and {total_threads} threads...\n"
        )

        WatchedThread.objects.all().delete()

        total_watched_threads = total_users * total_threads
        processed_count = 0

        start_time = time.time()
        show_progress(self, processed_count, total_watched_threads)

        for user in User.objects.iterator(chunk_size=50):
            for thread in Thread.objects.iterator(chunk_size=50):
                WatchedThread.objects.create(
                    user=user,
                    category_id=thread.category_id,
                    thread=thread,
                    send_emails=random.choice((True, False)),
                    read_time=thread.last_post_on,
                )

                processed_count += 1
                show_progress(self, processed_count, total_watched_threads)

        total_time = time.time() - start_time
        total_humanized = time.strftime("%H:%M:%S", time.gmtime(total_time))
        message = "\nSuccessfully created %s watched threads in %s"
        self.stdout.write(message % (total_watched_threads, total_humanized))
