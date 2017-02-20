import random
import sys
from datetime import timedelta

from faker import Factory

from django.core.management.base import BaseCommand
from django.utils import timezone

from misago.core.management.progressbar import show_progress
from misago.users.models import Ban


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
    if test_type == Ban.USERNAME:
        return fake_username_ban(fake)
    elif test_type == Ban.EMAIL:
        return fake_email_ban(fake)
    elif test_type == Ban.IP:
        return fake_ip_ban(fake)


class Command(BaseCommand):
    help = 'Creates random fakey bans for testing purposes'

    def handle(self, *args, **options):
        try:
            fake_bans_to_create = int(args[0])
        except IndexError:
            fake_bans_to_create = 5
        except ValueError:
            self.stderr.write("\nOptional argument should be integer.")
            sys.exit(1)

        fake = Factory.create()

        message = 'Creating %s fake bans...\n'
        self.stdout.write(message % fake_bans_to_create)

        message = '\n\nSuccessfully created %s fake bans'

        created_count = 0
        show_progress(self, created_count, fake_bans_to_create)
        for _ in range(fake_bans_to_create):
            ban = Ban(check_type=random.randint(Ban.USERNAME, Ban.IP))
            ban.banned_value = create_fake_test(fake, ban.check_type)

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
            show_progress(self, created_count, fake_bans_to_create)

        self.stdout.write(message % created_count)
