import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils import timezone
from faker import Factory
from misago.users.models import Ban, BAN_USERNAME, BAN_EMAIL, BAN_IP


def fake_username_ban(fake):
    fake_value = fake.first_name()

    if random.randint(0, 100) < 31:
        fake_value = '%s*' % fake_value
    elif random.randint(0, 100) < 31:
        fake_value = '*%s' % fake_value
    elif random.randint(0, 100) < 31:
        fake_value = list(fake_value)
        fake_value.insert(random.randint(0, len(fake_value) - 1), '*')
        fake_value = ''.join(fake_value)

    return fake_value


def fake_email_ban(fake):
    if random.randint(0, 100) < 35:
        return '*@%s' % fake.domain_name()
    else:
        return fake.email()


def fake_ip_ban(fake):
    if random.randint(0, 1):
        fake_value = fake.ipv4()
        if random.randint(0, 100) < 35:
            fake_value = fake_value.split('.')
            fake_value = '.'.join(fake_value[:random.randint(1, 3)])
            fake_value = '%s.*' % fake_value
        elif random.randint(0, 100) < 35:
            fake_value = fake_value.split('.')
            fake_value = '.'.join(fake_value[random.randint(1, 3):])
            fake_value = '*.%s' % fake_value
        elif random.randint(0, 100) < 35:
            fake_value = fake_value.split('.')
            fake_value[random.randint(0, 3)] = '*'
            fake_value = '.'.join(fake_value)
    else:
        fake_value = fake.ipv6()

        if random.randint(0, 100) < 35:
            fake_value = fake_value.split(':')
            fake_value = ':'.join(fake_value[:random.randint(1, 7)])
            fake_value = '%s:*' % fake_value
        elif random.randint(0, 100) < 35:
            fake_value = fake_value.split(':')
            fake_value = ':'.join(fake_value[:random.randint(1, 7)])
            fake_value = '*:%s' % fake_value
        elif random.randint(0, 100) < 35:
            fake_value = fake_value.split(':')
            fake_value[random.randint(0, 7)] = '*'
            fake_value = ':'.join(fake_value)

    return fake_value


def create_fake_test(fake, test_type):
    if test_type == BAN_USERNAME:
        return fake_username_ban(fake)
    elif test_type == BAN_EMAIL:
        return fake_email_ban(fake)
    elif test_type == BAN_IP:
        return fake_ip_ban(fake)


class Command(BaseCommand):
    help = 'Creates plenty of random fakey bans for testing purposes'

    def handle(self, *args, **options):
        fake_bans_to_create = 100000
        fake = Factory.create()

        message = 'Attempting to create %s fake bans!'
        self.stdout.write(message % fake_bans_to_create)

        message = 'Successfully created %s fake bans!'

        created_count = 0
        for i in xrange(fake_bans_to_create):
            ban = Ban(test=random.randint(BAN_USERNAME, BAN_IP))
            ban.banned_value = create_fake_test(fake, ban.test)

            if random.randint(0, 10) == 0:
                ban.user_message = fake.sentence()

            if random.randint(0, 10) == 0:
                ban.staff_message = fake.sentence()

            if random.randint(0, 1):
                # Lets make ban temporary
                ban_length = timedelta(days=random.randint(0, 300))
                if random.randint(0, 1):
                    ban.valid_until = timezone.now().date() - ban_length
                else:
                    ban.valid_until = timezone.now().date() + ban_length

            ban.save()

            created_count += 1
            if created_count % 100 == 0:
                self.stdout.write(message % created_count)

        self.stdout.write(message % Vans.objects.all().count())
