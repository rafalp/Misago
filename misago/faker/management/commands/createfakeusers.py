import random, sys

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from faker import Factory
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

        message = 'Attempting to create %s fake user accounts!'
        self.stdout.write(message % fake_users_to_create)

        message = 'Successfully created %s fake user accounts!'

        created_count = 0
        for i in xrange(fake_users_to_create + 1):
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
                if (created_count * 100 / fake_users_to_create) % 10 == 0:
                    self.stdout.write(message % created_count)

        self.stdout.write(message % created_count)
