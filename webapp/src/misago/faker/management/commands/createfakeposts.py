import random
import time

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Factory

from ....categories.models import Category
from ....core.management.progressbar import show_progress
from ....core.pgutils import chunk_queryset
from ....threads.models import Thread
from ...posts import get_fake_hidden_post, get_fake_post, get_fake_unapproved_post

User = get_user_model()


class Command(BaseCommand):
    help = "Creates random posts for dev and testing purposes."

    def add_arguments(self, parser):
        parser.add_argument(
            "posts", help="number of posts to create", nargs="?", type=int, default=5
        )

    def handle(self, *args, **options):
        items_to_create = options["posts"]
        fake = Factory.create()

        message = "Creating %s fake posts...\n"
        self.stdout.write(message % items_to_create)

        created_posts = 0
        start_time = time.time()
        show_progress(self, created_posts, items_to_create)

        while created_posts < items_to_create:
            thread = Thread.objects.order_by("?")[:1].first()

            # 10% chance poster is anonymous
            if random.randint(0, 100) > 90:
                poster = None
            else:
                poster = User.objects.order_by("?").last()

            # There's 5% chance post is unapproved
            if random.randint(0, 100) > 90:
                get_fake_unapproved_post(fake, thread, poster)

            # There's further 5% chance post is hidden
            elif random.randint(0, 100) > 95:
                if random.randint(0, 100) > 90:
                    hidden_by = None
                else:
                    hidden_by = User.objects.order_by("?").last()

                get_fake_hidden_post(fake, thread, poster, hidden_by)

            # Default, standard post
            else:
                get_fake_post(fake, thread, poster)

            created_posts += 1
            show_progress(self, created_posts, items_to_create, start_time)

        for thread in chunk_queryset(Thread.objects.all()):
            thread.synchronize()
            thread.save()

        for category in Category.objects.all():
            category.synchronize()
            category.save()

        total_time = time.time() - start_time
        total_humanized = time.strftime("%H:%M:%S", time.gmtime(total_time))
        message = "\nSuccessfully created %s fake posts in %s"
        self.stdout.write(message % (created_posts, total_humanized))
