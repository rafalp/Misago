import random
import time

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Factory

from ....categories.models import Category
from ....core.management.progressbar import show_progress
from ....threads.models import Thread
from ...threads import (
    get_fake_closed_thread,
    get_fake_hidden_thread,
    get_fake_thread,
    get_fake_unapproved_thread,
)

User = get_user_model()


class Command(BaseCommand):
    help = "Creates random threads for dev and testing purposes."

    def add_arguments(self, parser):
        parser.add_argument(
            "threads",
            help="number of threads to create",
            nargs="?",
            type=int,
            default=5,
        )

    def handle(
        self, *args, **options
    ):  # pylint: disable=too-many-locals, too-many-branches
        items_to_create = options["threads"]
        fake = Factory.create()

        categories = list(Category.objects.all_categories())

        message = "Creating %s fake threads...\n"
        self.stdout.write(message % items_to_create)

        created_threads = 0
        start_time = time.time()
        show_progress(self, created_threads, items_to_create)

        while created_threads < items_to_create:
            category = random.choice(categories)

            # 10% chance thread poster is anonymous
            if random.randint(0, 100) > 90:
                starter = None
            else:
                starter = User.objects.order_by("?").last()

            # There's 10% chance thread is closed
            if random.randint(0, 100) > 90:
                thread = get_fake_closed_thread(fake, category, starter)

            # There's further 5% chance thread is hidden
            elif random.randint(0, 100) > 95:
                if random.randint(0, 100) > 90:
                    hidden_by = None
                else:
                    hidden_by = User.objects.order_by("?").last()

                thread = get_fake_hidden_thread(fake, category, starter, hidden_by)

            # And further 5% chance thread is unapproved
            elif random.randint(0, 100) > 95:
                thread = get_fake_unapproved_thread(fake, category, starter)

            # Default, standard thread
            else:
                thread = get_fake_thread(fake, category, starter)

            thread.synchronize()
            thread.save()

            created_threads += 1
            show_progress(self, created_threads, items_to_create, start_time)

        pinned_threads = random.randint(0, int(created_threads * 0.025)) or 1
        self.stdout.write("\nPinning %s threads..." % pinned_threads)

        for _ in range(0, pinned_threads):
            thread = Thread.objects.order_by("?")[:1][0]
            if random.randint(0, 100) > 90:
                thread.weight = 2
            else:
                thread.weight = 1
            thread.save()

        for category in categories:
            category.synchronize()
            category.save()

        total_time = time.time() - start_time
        total_humanized = time.strftime("%H:%M:%S", time.gmtime(total_time))
        message = "\nSuccessfully created %s fake threads in %s"
        self.stdout.write(message % (created_threads, total_humanized))
