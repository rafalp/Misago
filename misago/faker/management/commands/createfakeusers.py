import random
from faker import Factory
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from misago.users.models import Rank


class Command(BaseCommand):
    help = 'Creates plenty of random fakey users for testing purposes'

    def handle(self, *args, **options):
        fake_users_to_create = 100000
        fake = Factory.create()
        User = get_user_model()

        ranks = [r for r in Rank.objects.all()]

        message = 'Attempting to create %s fake user accounts!'
        self.stdout.write(message % fake_users_to_create)

        message = 'Successfully created %s fake user accounts!'

        created_count = 0
        for i in xrange(fake_users_to_create):
            try:
                kwargs = {
                    'rank': random.choice(ranks),
                }

                User.objects.create_user(fake.first_name(), fake.email(),
                                         'pass123', **kwargs)
            except (ValidationError, IntegrityError):
                pass
            else:
                created_count += 1
                if created_count % 100 == 0:
                    self.stdout.write(message % created_count)

        self.stdout.write(message % User.objects.all().count())
