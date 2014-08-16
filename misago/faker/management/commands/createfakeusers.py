import random
import sys

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from faker import Factory

from misago.core.management.progressbar import show_progress
from misago.users.models import Rank


class Command(BaseCommand):
    help = 'Creates random fakey users for testing purposes'

    def handle(self, *args, **options):
        try:
            fake_users_to_create = int(args[0])
        except IndexError:
            fake_users_to_create = 5
        except ValueError:
            self.stderr.write("\nOptional argument should be integer.")
            sys.exit(1)

        fake = Factory.create()
        User = get_user_model()

        ranks = [r for r in Rank.objects.all()]

        message = 'Creating %s fake user accounts...\n'
        self.stdout.write(message % fake_users_to_create)

        message = '\n\nSuccessfully created %s fake user accounts'

        created_count = 0
        show_progress(self, created_count, fake_users_to_create)
        for i in xrange(fake_users_to_create):
            try:
                kwargs = {
                    'rank': random.choice(ranks),
                }

                User.objects.create_user(fake.first_name(), fake.email(),
                                         'pass123', set_default_avatar=True,
                                         **kwargs)
            except (ValidationError, IntegrityError):
                pass
            else:
                created_count += 1
                show_progress(self, created_count, fake_users_to_create)

        self.stdout.write(message % created_count)
