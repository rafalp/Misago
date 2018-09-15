import random
import time

from faker import Factory

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from misago.core.management.progressbar import show_progress
from misago.users.avatars import dynamic, gallery
from misago.users.models import Rank


UserModel = get_user_model()


class Command(BaseCommand):
    help = "Creates fake users for dev and testing purposes."

    def add_arguments(self, parser):
        parser.add_argument(
            'users',
            help="number of users to create",
            nargs='?',
            type=int,
            default=5,
        )

    def handle(self, *args, **options):
        items_to_create = options['users']

        fake = Factory.create()

        ranks = [r for r in Rank.objects.all()]

        message = 'Creating %s fake user accounts...\n'
        self.stdout.write(message % items_to_create)

        created_count = 0
        start_time = time.time()
        show_progress(self, created_count, items_to_create)

        while created_count < items_to_create:
            try:
                possible_usernames = [
                    fake.first_name(),
                    fake.last_name(),
                    fake.name().replace(' ', ''),
                    fake.user_name(),
                ]

                user = UserModel.objects.create_user(
                    random.choice(possible_usernames),
                    fake.email(),
                    'pass123',
                    set_default_avatar=False,
                    rank=random.choice(ranks),
                )

                dynamic.set_avatar(user)
                user.save(update_fields=['avatars'])
            except (ValidationError, IntegrityError):
                pass
            else:
                created_count += 1
                show_progress(self, created_count, items_to_create, start_time)

        total_time = time.time() - start_time
        total_humanized = time.strftime('%H:%M:%S', time.gmtime(total_time))
        message = '\n\nSuccessfully created %s fake user accounts in %s'
        self.stdout.write(message % (created_count, total_humanized))
