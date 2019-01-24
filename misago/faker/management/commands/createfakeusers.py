import random
import time

from django.core.management.base import BaseCommand
from faker import Factory

from ....core.management.progressbar import show_progress
from ....users.models import Rank
from ...users import (
    get_fake_inactive_user,
    get_fake_admin_activated_user,
    get_fake_banned_user,
    get_fake_user,
)


class Command(BaseCommand):
    help = "Creates fake users for dev and testing purposes."

    def add_arguments(self, parser):
        parser.add_argument(
            "users", help="number of users to create", nargs="?", type=int, default=5
        )

    def handle(self, *args, **options):
        items_to_create = options["users"]

        fake = Factory.create()
        ranks = list(Rank.objects.all())

        message = "Creating %s fake user accounts...\n"
        self.stdout.write(message % items_to_create)

        created_count = 0
        start_time = time.time()
        show_progress(self, created_count, items_to_create)

        while created_count < items_to_create:
            rank = random.choice(ranks)
            if random.randint(0, 100) > 80:
                get_fake_inactive_user(fake, rank)
            elif random.randint(0, 100) > 90:
                get_fake_admin_activated_user(fake, rank)
            elif random.randint(0, 100) > 90:
                get_fake_banned_user(fake, rank)
            else:
                get_fake_user(fake, rank)

            created_count += 1
            show_progress(self, created_count, items_to_create, start_time)

        total_time = time.time() - start_time
        total_humanized = time.strftime("%H:%M:%S", time.gmtime(total_time))
        message = "\n\nSuccessfully created %s fake user accounts in %s"
        self.stdout.write(message % (created_count, total_humanized))
